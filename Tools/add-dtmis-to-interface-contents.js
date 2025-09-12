#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

/**
 * Script to add DTMIs to all DTDL interface contents (Properties, Relationships, Components, Commands, Telemetries)
 * and verify uniqueness of all DTMIs across the ontology.
 */

class DTMIGenerator {
    constructor() {
        this.usedDTMIs = new Set();
        this.conflicts = [];
        this.elementCounters = new Map(); // Track counters for each interface
    }

    /**
     * Generate a short, unique DTMI for an interface content element
     * @param {string} interfaceDTMI - The parent interface DTMI
     * @param {string} elementName - The name of the element
     * @param {string} elementType - The type of element (Property, Relationship, Component, Command, Telemetry, etc.)
     * @param {string} context - Optional context for nested elements
     * @returns {string} Generated DTMI
     */
    generateContentDTMI(interfaceDTMI, elementName, elementType, context = '') {
        // Remove version from interface DTMI to create base
        const baseInterfaceDTMI = interfaceDTMI.split(';')[0];
        
        // Initialize counter for this interface if not exists
        if (!this.elementCounters.has(baseInterfaceDTMI)) {
            this.elementCounters.set(baseInterfaceDTMI, 1);
        }
        
        // Try the simple approach first: base:elementName;1
        let simpleDTMI = `${baseInterfaceDTMI}:${elementName};1`;
        
        // If simple DTMI is not taken, use it
        if (!this.usedDTMIs.has(simpleDTMI)) {
            return simpleDTMI;
        }
        
        // If there's a conflict, use a counter-based approach for uniqueness
        let counter = this.elementCounters.get(baseInterfaceDTMI);
        let dtmi;
        
        do {
            // Generate short DTMI with context hint and counter
            const contextHint = context ? context.charAt(0).toUpperCase() : '';
            const typeHint = elementType.charAt(0).toUpperCase();
            dtmi = `${baseInterfaceDTMI}:${contextHint}${typeHint}${counter};1`;
            counter++;
        } while (this.usedDTMIs.has(dtmi));
        
        // Update counter for next use
        this.elementCounters.set(baseInterfaceDTMI, counter);
        
        return dtmi;
    }

    /**
     * Check if DTMI is unique and track it
     * @param {string} dtmi - The DTMI to check
     * @param {string} filePath - File path where the DTMI is found
     * @param {string} elementName - Name of the element
     * @returns {boolean} True if unique, false if conflict
     */
    trackDTMI(dtmi, filePath, elementName) {
        if (this.usedDTMIs.has(dtmi)) {
            this.conflicts.push({
                dtmi,
                filePath,
                elementName,
                message: `Duplicate DTMI: ${dtmi} in ${filePath} for element ${elementName}`
            });
            return false;
        }
        
        this.usedDTMIs.add(dtmi);
        return true;
    }

    /**
     * Process nested schema objects recursively (Map, Array, Object, etc.)
     * @param {Object} schema - The schema object
     * @param {string} interfaceDTMI - Parent interface DTMI
     * @param {string} parentName - Name of parent element
     * @param {string} schemaPath - Path to this schema for naming
     * @param {string} filePath - File path for error reporting
     * @returns {boolean} True if schema was modified
     */
    processNestedSchema(schema, interfaceDTMI, parentName, schemaPath, filePath) {
        if (!schema || typeof schema !== 'object') return false;
        
        let modified = false;
        
        // Process the schema itself if it has @type but no @id
        if (schema['@type'] && !schema['@id']) {
            const schemaType = Array.isArray(schema['@type']) ? schema['@type'][0] : schema['@type'];
            const complexSchemaTypes = ['Map', 'Array', 'Object', 'Enum'];
            
            if (complexSchemaTypes.includes(schemaType)) {
                const dtmi = this.generateContentDTMI(interfaceDTMI, parentName, 'Schema', schemaType);
                
                if (this.trackDTMI(dtmi, filePath, `${parentName}${schemaPath}${schemaType}`)) {
                    schema['@id'] = dtmi;
                    console.log(`Added DTMI to ${schemaType} schema '${parentName}': ${dtmi}`);
                    modified = true;
                }
            }
        }
        
        // Process Map-specific elements
        if (schema['@type'] === 'Map') {
            if (schema.mapKey && !schema.mapKey['@id'] && schema.mapKey.name) {
                const dtmi = this.generateContentDTMI(interfaceDTMI, schema.mapKey.name, 'MapKey', 'Map');
                
                if (this.trackDTMI(dtmi, filePath, schema.mapKey.name)) {
                    schema.mapKey['@id'] = dtmi;
                    console.log(`Added DTMI to MapKey '${schema.mapKey.name}': ${dtmi}`);
                    modified = true;
                }
            }
            
            if (schema.mapValue && !schema.mapValue['@id'] && schema.mapValue.name) {
                const dtmi = this.generateContentDTMI(interfaceDTMI, schema.mapValue.name, 'MapValue', 'Map');
                
                if (this.trackDTMI(dtmi, filePath, schema.mapValue.name)) {
                    schema.mapValue['@id'] = dtmi;
                    console.log(`Added DTMI to MapValue '${schema.mapValue.name}': ${dtmi}`);
                    modified = true;
                }
                
                // Recursively process nested schema in mapValue
                if (schema.mapValue.schema) {
                    if (this.processNestedSchema(schema.mapValue.schema, interfaceDTMI, schema.mapValue.name, 'Nested', filePath)) {
                        modified = true;
                    }
                }
            }
        }
        
        // Process Array-specific elements
        if (schema['@type'] === 'Array' && schema.elementSchema) {
            if (this.processNestedSchema(schema.elementSchema, interfaceDTMI, parentName, 'Array', filePath)) {
                modified = true;
            }
        }
        
        // Process Object fields
        if (schema['@type'] === 'Object' && Array.isArray(schema.fields)) {
            schema.fields.forEach((field, index) => {
                if (field.schema) {
                    if (this.processNestedSchema(field.schema, interfaceDTMI, parentName, 'Object', filePath)) {
                        modified = true;
                    }
                }
            });
        }
        
        // Process Enum values
        if (schema['@type'] === 'Enum' && Array.isArray(schema.enumValues)) {
            schema.enumValues.forEach(enumValue => {
                if (enumValue.name && !enumValue['@id']) {
                    const dtmi = this.generateContentDTMI(interfaceDTMI, enumValue.name, 'EnumValue', 'Enum');
                    
                    if (this.trackDTMI(dtmi, filePath, enumValue.name)) {
                        enumValue['@id'] = dtmi;
                        console.log(`Added DTMI to EnumValue '${enumValue.name}': ${dtmi}`);
                        modified = true;
                    }
                }
            });
        }
        
        return modified;
    }

    /**
     * Process a single content element (Property, Relationship, etc.)
     * @param {Object} element - The content element
     * @param {string} interfaceDTMI - Parent interface DTMI
     * @param {string} filePath - File path for error reporting
     * @returns {boolean} True if element was modified
     */
    processContentElement(element, interfaceDTMI, filePath) {
        let modified = false;
        
        // Skip if element already has @id, but still track it
        if (element['@id']) {
            this.trackDTMI(element['@id'], filePath, element.name || 'unnamed');
        } else {
            // Only process elements with @type and name
            if (element['@type'] && element.name) {
                const elementType = Array.isArray(element['@type']) ? element['@type'][0] : element['@type'];
                
                // Only process specific types
                const supportedTypes = ['Property', 'Relationship', 'Component', 'Command', 'Telemetry'];
                if (supportedTypes.includes(elementType)) {
                    const dtmi = this.generateContentDTMI(interfaceDTMI, element.name, elementType);
                    
                    if (this.trackDTMI(dtmi, filePath, element.name)) {
                        element['@id'] = dtmi;
                        console.log(`Added DTMI to ${elementType} '${element.name}': ${dtmi}`);
                        modified = true;
                    }
                }
            }
        }
        
        // Process nested schemas in the element
        if (element.schema) {
            if (this.processNestedSchema(element.schema, interfaceDTMI, element.name || 'unnamed', '', filePath)) {
                modified = true;
            }
        }
        
        return modified;
    }

    /**
     * Process all schemas in the schemas array
     * @param {Array} schemas - Array of schema objects
     * @param {string} interfaceDTMI - Parent interface DTMI
     * @param {string} filePath - File path for error reporting
     * @returns {boolean} True if any schemas were modified
     */
    processSchemas(schemas, interfaceDTMI, filePath) {
        if (!Array.isArray(schemas)) return false;

        let modified = false;
        schemas.forEach(schema => {
            if (schema['@id']) {
                this.trackDTMI(schema['@id'], filePath, schema.displayName?.en || 'unnamed schema');
            }
            
            // Process EnumValues in top-level schemas
            if (schema['@type'] === 'Enum' && Array.isArray(schema.enumValues)) {
                schema.enumValues.forEach(enumValue => {
                    if (enumValue.name && !enumValue['@id']) {
                        // Extract schema name from DTMI for better naming
                        const schemaName = schema['@id'] ? schema['@id'].split(':').pop().split(';')[0] : 'UnknownSchema';
                        const dtmi = this.generateContentDTMI(interfaceDTMI, enumValue.name, 'EnumValue', 'Schema');
                        
                        if (this.trackDTMI(dtmi, filePath, enumValue.name)) {
                            enumValue['@id'] = dtmi;
                            console.log(`Added DTMI to EnumValue '${enumValue.name}': ${dtmi}`);
                            modified = true;
                        }
                    }
                });
            }
        });

        return modified;
    }

    /**
     * Process a single DTDL file
     * @param {string} filePath - Path to the JSON file
     * @returns {Object} Processing result
     */
    processFile(filePath) {
        try {
            const fileContent = fs.readFileSync(filePath, 'utf8');
            const dtdlModel = JSON.parse(fileContent);

            // Verify this is a DTDL Interface
            if (dtdlModel['@type'] !== 'Interface' || !dtdlModel['@id']) {
                console.log(`Skipping ${filePath}: Not a DTDL Interface`);
                return { processed: false, modified: false, error: null };
            }

            const interfaceDTMI = dtdlModel['@id'];
            this.trackDTMI(interfaceDTMI, filePath, 'Interface');

            let modified = false;
            let processedElements = 0;

            // Process contents array
            if (Array.isArray(dtdlModel.contents)) {
                dtdlModel.contents.forEach(element => {
                    if (this.processContentElement(element, interfaceDTMI, filePath)) {
                        modified = true;
                        processedElements++;
                    }
                });
            }

            // Process schemas array
            if (this.processSchemas(dtdlModel.schemas, interfaceDTMI, filePath)) {
                modified = true;
            }

            // Write back to file if modified
            if (modified) {
                const updatedContent = JSON.stringify(dtdlModel, null, 2);
                fs.writeFileSync(filePath, updatedContent, 'utf8');
                console.log(`✓ Updated ${filePath} - Added DTMIs to ${processedElements} elements`);
            }

            return { 
                processed: true, 
                modified, 
                processedElements,
                error: null 
            };

        } catch (error) {
            console.error(`Error processing ${filePath}:`, error.message);
            return { processed: false, modified: false, error: error.message };
        }
    }

    /**
     * Recursively find all JSON files in a directory
     * @param {string} dirPath - Directory to search
     * @returns {Array<string>} Array of JSON file paths
     */
    findJsonFiles(dirPath) {
        const jsonFiles = [];
        
        const items = fs.readdirSync(dirPath);
        items.forEach(item => {
            const itemPath = path.join(dirPath, item);
            const stat = fs.statSync(itemPath);
            
            if (stat.isDirectory()) {
                jsonFiles.push(...this.findJsonFiles(itemPath));
            } else if (item.endsWith('.json')) {
                jsonFiles.push(itemPath);
            }
        });
        
        return jsonFiles;
    }

    /**
     * Process all DTDL files in the ontology directory or a single file
     * @param {string} ontologyPath - Path to the ontology directory or single file
     */
    processOntology(ontologyPath) {
        console.log(`Starting DTMI addition process for: ${ontologyPath}\n`);

        let jsonFiles = [];
        const stat = fs.statSync(ontologyPath);
        
        if (stat.isDirectory()) {
            jsonFiles = this.findJsonFiles(ontologyPath);
        } else if (ontologyPath.endsWith('.json')) {
            jsonFiles = [ontologyPath];
        } else {
            console.error(`Error: Path must be a directory or JSON file: ${ontologyPath}`);
            return;
        }
        
        console.log(`Found ${jsonFiles.length} JSON files\n`);

        let totalProcessed = 0;
        let totalModified = 0;
        let totalElements = 0;
        let errors = [];

        jsonFiles.forEach(filePath => {
            const result = this.processFile(filePath);
            if (result.processed) {
                totalProcessed++;
                if (result.modified) {
                    totalModified++;
                    totalElements += result.processedElements;
                }
            }
            if (result.error) {
                errors.push({ filePath, error: result.error });
            }
        });

        // Report results
        console.log('\n' + '='.repeat(80));
        console.log('PROCESSING COMPLETE');
        console.log('='.repeat(80));
        console.log(`Files processed: ${totalProcessed}`);
        console.log(`Files modified: ${totalModified}`);
        console.log(`Elements with DTMIs added: ${totalElements}`);
        console.log(`Total unique DTMIs tracked: ${this.usedDTMIs.size}`);

        if (errors.length > 0) {
            console.log(`\nErrors encountered: ${errors.length}`);
            errors.forEach(({ filePath, error }) => {
                console.log(`  - ${filePath}: ${error}`);
            });
        }

        if (this.conflicts.length > 0) {
            console.log(`\n⚠️  DTMI CONFLICTS DETECTED: ${this.conflicts.length}`);
            this.conflicts.forEach(conflict => {
                console.log(`  - ${conflict.message}`);
            });
        } else {
            console.log('\n✅ All DTMIs are unique!');
        }
    }
}

// Main execution
function main() {
    const args = process.argv.slice(2);
    
    if (args.length === 0) {
        console.log('Usage: node add-dtmis-to-interface-contents.js <ontology-directory-or-file>');
        console.log('Examples:');
        console.log('  node add-dtmis-to-interface-contents.js ./Ontology');
        console.log('  node add-dtmis-to-interface-contents.js ./Ontology/Syyclops/Asset/Asset.json');
        process.exit(1);
    }

    const ontologyPath = path.resolve(args[0]);
    
    if (!fs.existsSync(ontologyPath)) {
        console.error(`Error: Directory does not exist: ${ontologyPath}`);
        process.exit(1);
    }

    const stat = fs.statSync(ontologyPath);
    if (!stat.isDirectory() && !ontologyPath.endsWith('.json')) {
        console.error(`Error: Path must be a directory or JSON file: ${ontologyPath}`);
        process.exit(1);
    }

    const generator = new DTMIGenerator();
    generator.processOntology(ontologyPath);
}

// Run the script
if (require.main === module) {
    main();
}

module.exports = DTMIGenerator;

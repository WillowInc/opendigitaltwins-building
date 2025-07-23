const fs = require("fs");
const path = require("path");

/**
 * Converts camelCase to Title Case with spaces
 * Example: "AssetRelationshipRefObject" -> "Asset Relationship Ref Object"
 * Handles acronyms dynamically: "BuildingCBECS" -> "Building CBECS"
 * Handles multiple acronyms: "BuildingIECCClimate" -> "Building IECC Climate"
 */
function camelCaseToTitleCase(str) {
  // Handle special cases first
  if (str.includes("ID")) {
    str = str.replace(/ID/g, "Id");
  }
  if (str.includes("URL")) {
    str = str.replace(/URL/g, "Url");
  }

  let result = "";
  let i = 0;

  while (i < str.length) {
    if (str[i] === str[i].toUpperCase()) {
      // Found a capital letter
      let word = str[i];
      i++;

      // Check if this is part of an acronym (multiple consecutive capitals)
      while (i < str.length && str[i] === str[i].toUpperCase()) {
        word += str[i];
        i++;
      }

      // If we have an acronym, check if the last letter should be the start of the next word
      if (word.length > 1) {
        // Look ahead to see if the next character is lowercase
        if (i < str.length && str[i] === str[i].toLowerCase()) {
          // The last capital letter should be the start of the next word
          const acronym = word.slice(0, -1); // All but the last letter
          const nextWordStart = word.slice(-1); // The last letter

          if (result && result[result.length - 1] !== " ") {
            result += " ";
          }
          result += acronym;
          result += " ";
          result += nextWordStart + str[i];
          i++;
        } else {
          // It's a true acronym, add it as is
          if (result && result[result.length - 1] !== " ") {
            result += " ";
          }
          result += word;
        }
      } else {
        // Single capital letter - check if next character is lowercase
        if (i < str.length && str[i] === str[i].toLowerCase()) {
          // This is the start of a word
          if (result && result[result.length - 1] !== " ") {
            result += " ";
          }
          result += word + str[i];
          i++;
        } else {
          // This might be a single letter acronym or followed by another capital
          if (result && result[result.length - 1] !== " ") {
            result += " ";
          }
          result += word;
        }
      }
    } else {
      // Lowercase letter - continue building the current word
      result += str[i];
      i++;
    }
  }

  return result.trim();
}

/**
 * Extracts the schema name from a DTMI
 * Example: "dtmi:com:syyclops:AssetRelationshipRefObject;1" -> "AssetRelationshipRefObject"
 */
function extractSchemaName(dtmi) {
  const parts = dtmi.split(":");
  const lastPart = parts[parts.length - 1];
  return lastPart.split(";")[0];
}

/**
 * Processes a schema object and adds displayName if it doesn't exist
 */
function processSchema(schema) {
  if (schema["@id"] && !schema.displayName) {
    // Handle different schema types
    const schemaTypes = ["Interface", "Enum", "Object"];
    if (schemaTypes.includes(schema["@type"])) {
      const schemaName = extractSchemaName(schema["@id"]);
      const displayName = camelCaseToTitleCase(schemaName);
      schema.displayName = {
        en: displayName,
      };
      return true; // Indicates a change was made
    }
  }
  return false;
}

/**
 * Recursively processes all schemas in an object
 */
function processSchemas(obj, changes = []) {
  if (typeof obj !== "object" || obj === null) {
    return changes;
  }

  // If this is a schema object (has @id), process it
  if (obj["@id"]) {
    if (processSchema(obj)) {
      changes.push(`Added displayName to ${obj["@type"]}: ${obj["@id"]}`);
    }
  }

  // Special handling for the schemas array
  if (Array.isArray(obj.schemas)) {
    obj.schemas.forEach((schema, index) => {
      if (processSchema(schema)) {
        changes.push(
          `Added displayName to schema in schemas array: ${schema["@id"]}`
        );
      }
    });
  }

  // Recursively process all properties
  for (const key in obj) {
    if (Array.isArray(obj[key])) {
      obj[key].forEach((item, index) => {
        processSchemas(item, changes);
      });
    } else {
      processSchemas(obj[key], changes);
    }
  }

  return changes;
}

/**
 * Processes a single JSON file
 */
function processFile(filePath) {
  try {
    console.log(`Processing: ${filePath}`);
    const content = fs.readFileSync(filePath, "utf8");
    const data = JSON.parse(content);

    const changes = processSchemas(data);

    if (changes.length > 0) {
      // Write back to file with proper formatting
      fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
      console.log(`  ✓ Updated ${changes.length} schemas`);
      changes.forEach((change) => console.log(`    - ${change}`));
    } else {
      console.log(`  - No changes needed`);
    }

    return changes.length;
  } catch (error) {
    console.error(`  ✗ Error processing ${filePath}:`, error.message);
    return 0;
  }
}

/**
 * Recursively finds all JSON files in a directory
 */
function findJsonFiles(dir, files = []) {
  const items = fs.readdirSync(dir);

  for (const item of items) {
    const fullPath = path.join(dir, item);
    const stat = fs.statSync(fullPath);

    if (stat.isDirectory()) {
      findJsonFiles(fullPath, files);
    } else if (item.endsWith(".json")) {
      files.push(fullPath);
    }
  }

  return files;
}

/**
 * Main function
 */
function main() {
  const ontologyDir = path.join(__dirname, "..", "Ontology");

  if (!fs.existsSync(ontologyDir)) {
    console.error("Ontology directory not found");
    process.exit(1);
  }

  console.log("Finding JSON files...");
  const jsonFiles = findJsonFiles(ontologyDir);
  console.log(`Found ${jsonFiles.length} JSON files\n`);

  let totalChanges = 0;
  let processedFiles = 0;

  for (const file of jsonFiles) {
    const changes = processFile(file);
    if (changes > 0) {
      totalChanges += changes;
      processedFiles++;
    }
  }

  console.log(`\nSummary:`);
  console.log(`- Processed ${jsonFiles.length} files`);
  console.log(`- Updated ${processedFiles} files`);
  console.log(`- Added ${totalChanges} displayName fields`);
}

if (require.main === module) {
  main();
}

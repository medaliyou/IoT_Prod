mongo  –username "admin" –password "godmode" –authenticationDatabase admin --eval "db.getMongo().getDBNames().forEach(function(dbName){ if (dbName.startsWith('IoT')) printjson(db.getSiblingDB(dbName).dropDatabase())  })"


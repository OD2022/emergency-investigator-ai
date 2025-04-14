from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class HospitalGraphUpdater:
    def __init__(self):
        # Get Neo4j credentials from environment variables
        uri = os.getenv("NEO4J_URI")
        user = os.getenv("NEO4J_USERNAME")
        password = os.getenv("NEO4J_PASSWORD")
        
        # Initialize the Neo4j driver
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Close the connection to the database
        self.driver.close()

    def update_hospital_details(self, hospital_name, address, telephone_number):
        # Update a hospital node with address and telephone_number
        with self.driver.session() as session:
            session.execute_write(self._update_hospital_node, hospital_name, address, telephone_number)

    @staticmethod
    def _update_hospital_node(tx, hospital_name, address, telephone_number):
        # Cypher query to update hospital with address and telephone number
        query = (
            "MATCH (h:Hospital {name: $hospital_name}) "
            "SET h.address = $address, h.telephone_number = $telephone_number"
        )
        tx.run(query, hospital_name=hospital_name, address=address, telephone_number=telephone_number)

    def update_all_hospitals(self, hospitals_info):
        # Update multiple hospitals with provided information
        with self.driver.session() as session:
            for hospital_name, info in hospitals_info.items():
                address = info.get('address')
                telephone_number = info.get('telephone_number')
                session.execute_write(self._update_hospital_node, hospital_name, address, telephone_number)

# Example usage
if __name__ == "__main__":
    # Create an instance of the updater class
    updater = HospitalGraphUpdater()

    # Example data for updating hospitals
    hospitals_info = {
        "City Hospital": {
            "address": "123 Main Street, Accra",
            "telephone_number": "+233 30 123 4567"
        },
        "Medical Center": {
            "address": "456 Medical Rd, Kumasi",
            "telephone_number": "+233 32 987 6543"
        },
        "Health Clinic": {
            "address": "789 Health Blvd, Takoradi",
            "telephone_number": "+233 31 234 5678"
        }
    }

    # Update all hospitals with the given information
    updater.update_all_hospitals(hospitals_info)

    # Close the connection
    updater.close()

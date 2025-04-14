from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class HospitalGraph:
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

    def create_hospital(self, hospital_name, opening_hours, closing_hours, staff_count, region, latitude, longitude, address, telephone_number):
    # Create a hospital node and link it to location with address and telephone_number
        with self.driver.session() as session:
            session.execute_write(self._create_hospital_node, hospital_name, opening_hours, closing_hours, staff_count, region, latitude, longitude, address, telephone_number)

    @staticmethod
    def _create_hospital_node(tx, hospital_name, opening_hours, closing_hours, staff_count, region, latitude, longitude, address, telephone_number):
    # Cypher query to create a hospital node with address and telephone_number and link to location
        query = (
        "CREATE (h:Hospital {name: $hospital_name, opening_hours: $opening_hours, closing_hours: $closing_hours, "
        "staff_count: $staff_count, address: $address, telephone_number: $telephone_number}) "
        "WITH h "
        "MERGE (l:Location {region: $region, latitude: $latitude, longitude: $longitude}) "
        "MERGE (h)-[:LOCATED_IN]->(l)"
    )
        tx.run(query, hospital_name=hospital_name, opening_hours=opening_hours, closing_hours=closing_hours, 
           staff_count=staff_count, address=address, telephone_number=telephone_number, 
           region=region, latitude=latitude, longitude=longitude)


    def create_professional(self, professional_name):
        # Create a professional node
        with self.driver.session() as session:
            session.execute_write(self._create_professional_node, professional_name)

    @staticmethod
    def _create_professional_node(tx, professional_name):
        # Create a professional node
        query = "CREATE (p:Professional {name: $professional_name})"
        tx.run(query, professional_name=professional_name)

    def create_equipment(self, equipment_name):
        # Create equipment node
        with self.driver.session() as session:
            session.execute_write(self._create_equipment_node, equipment_name)

    @staticmethod
    def _create_equipment_node(tx, equipment_name):
        # Create an equipment node
        query = "CREATE (e:Equipment {name: $equipment_name})"
        tx.run(query, equipment_name=equipment_name)

    def create_service(self, service_name):
        # Create service node
        with self.driver.session() as session:
            session.execute_write(self._create_service_node, service_name)

    @staticmethod
    def _create_service_node(tx, service_name):
        # Create a service node
        query = "CREATE (s:Service {name: $service_name})"
        tx.run(query, service_name=service_name)

    def link_hospital_to_professional(self, hospital_name, professional_name):
        # Link hospital to professional
        with self.driver.session() as session:
            session.execute_write(self._link_hospital_to_professional, hospital_name, professional_name)

    @staticmethod
    def _link_hospital_to_professional(tx, hospital_name, professional_name):
        # Create a relationship between hospital and professional
        query = (
            "MATCH (h:Hospital {name: $hospital_name}), (p:Professional {name: $professional_name}) "
            "MERGE (h)-[:HAS_PROFESSIONAL]->(p)"
        )
        tx.run(query, hospital_name=hospital_name, professional_name=professional_name)

    def link_hospital_to_equipment(self, hospital_name, equipment_name):
        # Link hospital to equipment
        with self.driver.session() as session:
            session.execute_write(self._link_hospital_to_equipment, hospital_name, equipment_name)

    @staticmethod
    def _link_hospital_to_equipment(tx, hospital_name, equipment_name):
        # Create a relationship between hospital and equipment
        query = (
            "MATCH (h:Hospital {name: $hospital_name}), (e:Equipment {name: $equipment_name}) "
            "MERGE (h)-[:HAS_EQUIPMENT]->(e)"
        )
        tx.run(query, hospital_name=hospital_name, equipment_name=equipment_name)

    def link_hospital_to_service(self, hospital_name, service_name):
        # Link hospital to service
        with self.driver.session() as session:
            session.execute_write(self._link_hospital_to_service, hospital_name, service_name)

    @staticmethod
    def _link_hospital_to_service(tx, hospital_name, service_name):
        # Create a relationship between hospital and service
        query = (
            "MATCH (h:Hospital {name: $hospital_name}), (s:Service {name: $service_name}) "
            "MERGE (h)-[:OFFERS]->(s)"
        )
        tx.run(query, hospital_name=hospital_name, service_name=service_name)

    def query_hospitals(self, region, service_name, professional_name, opening_hour_start, opening_hour_end, min_staff_count):
        # Query hospitals based on criteria
        with self.driver.session() as session:
            result = session.execute_read(self._query_hospitals, region, service_name, professional_name, opening_hour_start, opening_hour_end, min_staff_count)
            return result

    @staticmethod
    def _query_hospitals(tx, region, service_name, professional_name, opening_hour_start, opening_hour_end, min_staff_count):
        # Cypher query to find hospitals based on the provided criteria
        query = (
            "MATCH (h:Hospital)-[:LOCATED_IN]->(l:Location), (h)-[:OFFERS]->(s:Service), "
            "(h)-[:HAS_PROFESSIONAL]->(p:Professional) "
            "WHERE l.region = $region AND s.name = $service_name AND p.name = $professional_name "
            "AND h.opening_hours >= $opening_hour_start AND h.closing_hours <= $opening_hour_end "
            "AND h.staff_count >= $min_staff_count "
            "RETURN h.name AS hospital_name, l.region AS region, h.opening_hours AS opening_hours, "
            "h.closing_hours AS closing_hours, h.staff_count AS staff_count"
        )
        result = tx.run(query, region=region, service_name=service_name, professional_name=professional_name, 
                        opening_hour_start=opening_hour_start, opening_hour_end=opening_hour_end, min_staff_count=min_staff_count)
        return [record["hospital_name"] for record in result]



# Example of how to use the HospitalGraph class
# if __name__ == "__main__":
#     graph = HospitalGraph()

#     # Create nodes and link relationships
#     graph.create_hospital("City Hospital", "08:00 AM", "10:00 PM", 120, "Greater Accra", 5.6037, 0.1870)
#     graph.create_service("Orthopedics")
#     graph.create_professional("Surgeon")
#     graph.create_equipment("X-ray")

#     graph.link_hospital_to_service("City Hospital", "Orthopedics")
#     graph.link_hospital_to_professional("City Hospital", "Surgeon")
#     graph.link_hospital_to_equipment("City Hospital", "X-ray")

#     # Query hospitals with given criteria
#     result = graph.query_hospitals("Greater Accra", "Orthopedics", "Surgeon", "08:00 AM", "10:00 PM", 20)
#     print(result)

#     graph.close()

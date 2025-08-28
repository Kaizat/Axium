import json
import os
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

class StorageService:
    """Service for storing user inputs and LLM outputs in JSON format"""
    
    def __init__(self, storage_file: str = "recipe_interactions.json"):
        self.storage_file = storage_file
        self.ensure_storage_file_exists()
    
    def ensure_storage_file_exists(self):
        """Create storage file if it doesn't exist"""
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump({"interactions": []}, f, indent=2)
    
    def store_interaction(self, 
                         user_ingredients: List[str], 
                         llm_response: str, 
                         parsed_recipes: List[Dict], 
                         success: bool,
                         error_message: str = None) -> str:
        """Store a complete user interaction with LLM"""
        
        interaction_id = self.generate_interaction_id()
        
        interaction_data = {
            "interaction_id": interaction_id,
            "timestamp": datetime.now().isoformat(),
            "user_input": {
                "ingredients": user_ingredients,
                "ingredient_count": len(user_ingredients)
            },
            "llm_interaction": {
                "raw_response": llm_response,
                "response_length": len(llm_response) if llm_response else 0,
                "response_type": type(llm_response).__name__
            },
            "parsed_output": {
                "recipes": parsed_recipes,
                "recipe_count": len(parsed_recipes) if parsed_recipes else 0,
                "success": success
            },
            "metadata": {
                "error_message": error_message,
                "processing_status": "success" if success else "failed"
            }
        }
        
        # Load existing data
        with open(self.storage_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Add new interaction
        data["interactions"].append(interaction_data)
        
        # Save updated data
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 StorageService - Interaction {interaction_id} stored successfully")
        return interaction_id
    
    def generate_interaction_id(self) -> str:
        """Generate a unique interaction ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"recipe_interaction_{timestamp}"
    
    def get_all_interactions(self) -> List[Dict]:
        """Retrieve all stored interactions"""
        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("interactions", [])
        except FileNotFoundError:
            return []
    
    def get_interaction_by_id(self, interaction_id: str) -> Dict:
        """Retrieve a specific interaction by ID"""
        interactions = self.get_all_interactions()
        for interaction in interactions:
            if interaction.get("interaction_id") == interaction_id:
                return interaction
        return None
    
    def get_recent_interactions(self, limit: int = 10) -> List[Dict]:
        """Get the most recent interactions"""
        interactions = self.get_all_interactions()
        return interactions[-limit:] if interactions else []
    
    def get_storage_stats(self) -> Dict:
        """Get statistics about stored data"""
        interactions = self.get_all_interactions()
        
        if not interactions:
            return {"total_interactions": 0}
        
        total_interactions = len(interactions)
        successful_interactions = sum(1 for i in interactions if i["parsed_output"]["success"])
        failed_interactions = total_interactions - successful_interactions
        
        total_recipes_generated = sum(i["parsed_output"]["recipe_count"] for i in interactions)
        
        return {
            "total_interactions": total_interactions,
            "successful_interactions": successful_interactions,
            "failed_interactions": failed_interactions,
            "success_rate": (successful_interactions / total_interactions) * 100 if total_interactions > 0 else 0,
            "total_recipes_generated": total_recipes_generated,
            "average_recipes_per_interaction": total_recipes_generated / successful_interactions if successful_interactions > 0 else 0,
            "storage_file": self.storage_file,
            "file_size_bytes": os.path.getsize(self.storage_file) if os.path.exists(self.storage_file) else 0
        }
    
    def export_interactions_to_json(self, filename: str = None) -> str:
        """Export all interactions to a timestamped JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recipe_export_{timestamp}.json"
        
        interactions = self.get_all_interactions()
        
        export_data = {
            "export_info": {
                "timestamp": datetime.now().isoformat(),
                "total_interactions": len(interactions),
                "exported_by": "Smart Recipe Analyzer"
            },
            "interactions": interactions
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"📤 StorageService - Exported {len(interactions)} interactions to {filename}")
        return filename

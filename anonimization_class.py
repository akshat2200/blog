#!/usr/bin/env python
# coding: utf-8

# In[1]:


class Encoder:
    """
    Anonimization of categorical column
        - Column AnonimizedCol to be Anonimized
            * Anonimize it by creating another column with ids corresponding to categories
            * save the disctionary of mappings
            * Allow for adding new mappings in case of previously not seen categories
    """
        
    def __init__(self, mapping = {}):
        self.value_to_id = mapping
        self.id_to_value = {id : value for value, id in self.value_to_id.items()}
        if len(mapping.values()) > 0:
            self.next_id = pd.Series(list(data.values())).str.extract(r"Secret (\d+).").astype(int).max().item() + 1
        else:
            self.next_id = 0
            
    def fit(self, values):
        self.next_id = 0
        self.value_to_id = {}
        
        val_set = set(values)
        for element in val_set:
            self.value_to_id[element] = f"Secret {self.next_id}"
            self.next_id += 1
            
        self.id_to_value = {id : value for value, id in self.value_to_id.items()}
        return self
    
    def update(self, values):
        key_set = set(self.value_to_id.keys())
        val_set = set(values)
        diff_set = val_set.difference(key_set)
        
        for element in diff_set:
            self.value_to_id[element] = f"Secret {self.next_id}"
            self.id_to_value[f"Secret {self.next_id}"] = element
            self.next_id += 1
        return self
    
    def encode(self, values):
        self.update(values)
        return [self.value_to_id[value] for value in values]
    
    def decode(self, ids):
        
        try:
            return [self.id_to_value[id] for id in ids]
        except:
            raise Exception("Encoder encountered unknown ids")
            
    def save_mapping(self, filename):
        import json
        with open(filename, 'w') as fp:
            json.dump(self.value_to_id, fp)
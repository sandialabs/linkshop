service Link {
	string createLinko(1: string commands, 2: string ontology, 3: string abstraction, 4: string linkograph, 5: string unique_id),
        string drawLinko(1: string linkograph, 2: string unique_id),
        string saveFile(1: string fileName, 2: string fileContent, 3: string unique_id),
        string fileList(1: string fileType, 2: string unique_id),
        string loadFile(1: string fileName, 2: string fileType, 3: string unique_id),
	string getStats(1: string fileName, 2: i32 startRange, 3: i32 stopRange, 4: string unique_id),
	string performOntologyRefinement(1: string linkograph, 2: string ontology, 3: i32 max_changes, 4: string unique_id),
}

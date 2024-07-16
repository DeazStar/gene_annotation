MERGE (ENSG00000101349: gene {type: 'gene', id: 'ENSG00000101349', gene_type: 'protein_coding', start: 9537370, end: 9839076, chr: 'chr20'});

MERGE (ENSG00000286740: gene {type: 'gene', id: 'ENSG00000286740', gene_type: 'protein_coding', start: 9562941, end: 9571257, chr: 'chr20'});

MERGE (ENST00000353224: transcript {type: 'transcript', id: 'ENST00000353224', transcript_id: 'ENST00000353224.10', transcript_name: 'ENST00000353224', transcript_type: 'protein_coding', start: 9537370, end: 9839076, chr: 'chr20'});

MERGE (ENST00000657954: transcript {type: 'transcript', id: 'ENST00000657954', transcript_id: 'ENST00000657954.1', transcript_name: 'ENST00000657954', transcript_type: 'protein_coding', start: 9562941, end: 9571257, chr: 'chr20'});

MATCH (gene1: gene {id: 'ENSG00000101349'}),
      (transcript1: transcript {transcript_id: 'ENST00000353224.10'})
MERGE (gene1)-[:transcribed_to {relationship: 'transcribed_to', source_url: 'www.example.com'}]->(transcript1);

MATCH (gene2: gene {id: 'ENSG00000286740'}),
      (transcript2: transcript {transcript_id: 'ENST00000657954.1'})
MERGE (gene2)-[:transcribed_to {relationship: 'transcribed_to', source_url: 'www.example.com'}]->(transcript2);

MERGE (Q9P286: protein {id: 'Q9P286', type: 'protein'});

MATCH (transcript1: transcript {id: 'ENST00000353224'}),
      (protein1: protein {id: 'Q9P286'})
MERGE (transcript1)-[:translates_to {relationship: 'translates_to', source_url: 'www.example.com'}]->(protein1)

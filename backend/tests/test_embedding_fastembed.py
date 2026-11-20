from fastembed_cloud import CloudTextEmbedding

# First run will auto-provision a free API key
model = CloudTextEmbedding(model_name="bge-m3")

embedding = model.query_embed("Mbura y'ibara ry'umuhondo")
print(f"Dimensions: {len(embedding)}")

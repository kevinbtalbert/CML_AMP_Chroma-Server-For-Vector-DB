# Chroma Server For Vector DB (Deployed as CML AMP)
This AMP creates an application to host a Chroma Server for Vector DB and Semantic Search, accessible via REST API and demonstrates how to use it with sample code.

![](/assets/catalog-entry.png)

## Requirements

### Environment Requirements
The lowest level of compatibility for Chroma, as stated by the documentation, is Python 3.10. Compatibility is not guaranteed with any lower version, therefore the recommended and supported version for this AMP is Python 3.10 to ensure all dependencies are met. Any deviation from this will require modifying `setup-chroma.sh` to support the version change, and possibly other PyPi-met dependencies as well.

### Resource Requirements
This AMP creates the following workloads with resource requirements:
- CML Session: `2 CPU, 8GB MEM`
- CML Jobs: `2 CPU, 8GB MEM`
- CML Application: `2 CPU, 8GB MEM`

### External Resources
This AMP requires pip packages and models from huggingface. Depending on your CML networking setup, you may need to whitelist some domains:
- pypi.python.org
- pypi.org
- pythonhosted.org
- huggingface.co

### Technologies Used
#### Open-Source Models and Utilities
- [all-mpnet-base-v2](https://huggingface.co/sentence-transformers/sentence-transformers/all-mpnet-base-v2/resolve/main/all-mpnet-base-v2.tar.gz)
- [Hugging Face transformers library](https://pypi.org/project/transformers/)
#### Vector Database
- [Chroma DB](https://docs.trychroma.com/)
#### Hosting Platform
- **CML Applications**

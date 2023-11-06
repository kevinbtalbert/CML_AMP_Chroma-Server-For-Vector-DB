# Chroma Server For Vector DB (Deployed as CML AMP)
This AMP creates an application to host a Chroma Server for Vector DB and Semantic Search, accessible via REST API and demonstrates how to use it with sample code.

![](/assets/catalog-entry.png)

## AMP Description
This AMP creates an "Application" in CML that is a Chroma server which can be accessed by the Chroma persistent client documented at the [Chroma Docs](https://docs.trychroma.com/reference/Client). Sample code in `4_session-sample-usage/SampleUsageofAPI.ipynb` demonstrates how to add and query documents from the Chroma server. Generated vectors are persisted to `chroma-data`.

In order for the server to be accessed outside of CML, you will need to ensure unauthenticated access is enabled such as shown below in the screenshots.

![](/assets/unauthenticated-access1.png)

If it does not appear in the Application settings, it may need to be enabled at an environment level as is shown below.

![](/assets/unauthenticated-access2.png)

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

## Deploying on CML
There are two ways to launch this prototype on CML:

1. **From Prototype Catalog** - Navigate to the Prototype Catalog on a CML workspace, select the "Chroma Server for Vector DB" tile, click "Launch as Project", click "Configure Project"
2. **As ML Prototype** - In a CML workspace, click "New Project", add a Project Name, select "ML Prototype" as the Initial Setup option, copy in the [repo URL](https://github.com/kevinbtalbert/CML_AMP_Chroma-Server-For-Vector-DB), click "Create Project", click "Configure Project"

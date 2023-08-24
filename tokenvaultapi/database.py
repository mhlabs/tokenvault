"""database"""
import sys

from google.cloud import firestore

# Project ID is determined by the GCLOUD_PROJECT environment variable
# mockfirestore can't be used for testing async code, remove when fixed
# if "pytest" in sys.argv[0]:
#     # testing db
#     from mockfirestore import AsyncMockFirestore
#     db = AsyncMockFirestore()
# else:
    # not a testing db
    # db = firestore.Client()  # pragma: no cover
db = firestore.AsyncClient()

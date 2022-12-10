from pydantic import EmailStr

def validation_email_candidato_exist(db, email: EmailStr, collection):

    collection_companies = db[collection]

    email_exist = False

    email_entity_exist = collection_companies.find_one({
        "email": email
    })

    if not email_entity_exist:
        return email_exist

    email_exist = True
    return email_exist


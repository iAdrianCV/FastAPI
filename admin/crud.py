from admin.schemas import AdminCreate

def list_admin(db_depends):
    collection_name=db_depends["admin"]
    admins=list(collection_name.find())
    return admins


def create_admin(admin: AdminCreate, db_depends):
    collection_name=db_depends["admin"]
    admin_dict = admin.dict()
    collection_name.insert_one(admin_dict)
    return admin_dict



# async def save_company(company: CompanyCreate, db_depends):
#     collection_name=db_depends["companies"]
#     collection_name.insert_one(company)

#     await simple_send(email=[company["email"]])
#     return company

def get_admin_by_email(db_depends,email_admin:str):
    collection_name=db_depends["admin"]
    admin=collection_name.find_one({'email':email_admin})
    return admin

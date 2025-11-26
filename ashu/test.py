 # Serve owner files (EID, Passport, Visa)
# @app.route("/owners/<int:owner_code>", methods=["GET"])
# def get_owner(owner_code):
#     conn = get_owners_db()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM owner WHERE owner_code=%s", (owner_code,))
#     owner = cursor.fetchone()
#     cursor.close()
#     conn.close()

#     if owner:
#         # Remove binary fields
#         for field in ["eid_image", "passport_copy", "res_visa"]:
#             owner[field] = None
#         return jsonify(owner)
#     else:
#         return jsonify({"error": "Owner not found"}), 404

# @app.template_filter('b64encode')
# def b64encode_filter(data):
#     import base64
#     if not data:
#         return ""
#     try:
#         if isinstance(data, (bytes, bytearray)):
#             return base64.b64encode(data).decode("utf-8")
#         elif isinstance(data, str) and os.path.exists(data):
#             with open(data, "rb") as f:
#                 return base64.b64encode(f.read()).decode("utf-8")
#     except Exception as e:
#         print("Error encoding image:", e)
#         return ""
 
# @app.route("/api/owners")
# def api_list_owners():
#     if "user" not in session:
#         return jsonify({"success": False, "message": "Not logged in"}), 401

#     sort_field = request.args.get("sort", "owner_code")
#     sort_order = request.args.get("order", "ASC")
#     valid_fields = ["owner_code","first_name","last_name","email","mobile_number","nationality"]
#     if sort_field not in valid_fields: sort_field = "owner_code"
#     if sort_order not in ["ASC","DESC"]: sort_order = "ASC"

#     conn = get_owners_db()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute(f"SELECT * FROM owner ORDER BY {sort_field} {sort_order}")
#     owners = cursor.fetchall()
#     cursor.close()
#     conn.close()

#     return jsonify({"success": True, "owners": owners})
  # ---------------- OWNER IMAGE ----------------
# @app.route("/owner_image/<owner_code>/<img_type>")
# def get_owner_image(owner_code, img_type):
#     conn = get_owners_db()
#     cursor = conn.cursor()
#     cursor.execute(
#         f"SELECT {img_type} FROM owner WHERE owner_code=%s",
#         (owner_code,)
#     )
#     result = cursor.fetchone()
#     cursor.close()
#     conn.close()

#     if result and result[0]:
#         return Response(result[0], mimetype="image/jpeg")
#     else:
#         return "No image", 404


#------------------list
# @app.route("/api/owners")
# def api_list_owners():
#     if "user" not in session:
#         return jsonify({"success": False, "message": "Not logged in"}), 401

#     sort_field = request.args.get("sort", "owner_code")
#     sort_order = request.args.get("order", "ASC")
#     valid_fields = ["owner_code","first_name","last_name","email","mobile_number","nationality"]
#     if sort_field not in valid_fields: sort_field = "owner_code"
#     if sort_order not in ["ASC","DESC"]: sort_order = "ASC"

#     conn = get_owners_db()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute(f"SELECT * FROM owner ORDER BY {sort_field} {sort_order}")
#     owners = cursor.fetchall()
#     cursor.close()
#     conn.close()

#     return jsonify({"success": True, "owners": owners})

# @app.route("/add_property", methods=["GET", "POST"])
# def add_property():
#     owner = None
#     show_form = False

#     if request.method == "POST":
#         if "search_owner" in request.form:
#             owner_code = request.form.get("owner_code")
#             conn = get_owners_db()
#             cursor = conn.cursor(dictionary=True)
#             cursor.execute("SELECT * FROM Owner WHERE owner_code=%s", (owner_code,))
#             owner = cursor.fetchone()
#             cursor.close()
#             conn.close()
#             if owner:
#                 show_form = True
#             else:
#                 flash(f"No owner found with code {owner_code}")

#         elif "add_property" in request.form:
#             form = request.form
#             files = request.files
#             owner_code = form.get("owner_code")

#             conn = get_owners_db()
#             cursor = conn.cursor()

#             # Auto-generate property_code
#             cursor.execute("SELECT MAX(property_code) AS max_id FROM property")
#             max_id = cursor.fetchone()[0] or 0
#             next_code = max_id + 1

#             columns = [
#                 "property_code","primary_owner_code","developer_name","building_name","property_type",
#                 "name","address1","address2","city","state","country","zip_code","municipality_number",
#                 "electricity_bill_number","water_bill_number","ownership_type","furnishing_status",
#                 "land_area","carpet_area","builtup_area","bedrooms","bathrooms","washrooms","facing",
#                 "car_parkings","servant_rooms","balconies","has_dishwasher","has_washing_machine",
#                 "property_value","year_of_construction","second_owner_code","expected_rent_value",
#                 "status","mtd_income","ytd_income","mtd_expense","ytd_expense","purchase_value",
#                 "construction_cost","renovation_cost","registration","transfer_fees","misc_expense",
#                 "created_by","creation_date","property_photo"
#             ]

#             values = []
#             for col in columns:
#                 if col == "property_code":
#                     values.append(next_code)
#                 elif col == "primary_owner_code":
#                     values.append(owner_code)
#                 elif col == "created_by":
#                     values.append(session.get("user", "admin"))
#                 elif col == "creation_date":
#                     values.append(date.today())
#                 elif col == "property_photo":
#                     file = files.get("property_photo")
#                     values.append(file.read() if file else None)
#                 elif col in [
#                     "land_area","carpet_area","builtup_area","bedrooms","bathrooms","washrooms",
#                     "car_parkings","servant_rooms","balconies","property_value","expected_rent_value",
#                     "mtd_income","ytd_income","mtd_expense","ytd_expense","purchase_value",
#                     "construction_cost","renovation_cost","registration","transfer_fees","misc_expense"
#                 ]:
#                     values.append(float(form.get(col) or 0))
#                 else:
#                     values.append(form.get(col) or None)

#             placeholders = ",".join(["%s"] * len(columns))
#             sql = f"INSERT INTO property ({','.join(columns)}) VALUES ({placeholders})"
#             cursor.execute(sql, tuple(values))
#             conn.commit()
#             cursor.close()
#             conn.close()
#             flash(f"✅ Property added successfully! Property Code: {next_code}")
#             return redirect(url_for("add_property"))

#     return render_template("add_property.html", owner=owner, show_form=show_form, today=date.today())
# #--------------property_modify--------------------
# # import base64
# # from datetime import date


# # ---------------------- DATABASE CONNECTION ----------------------
# # def get_owners_db():
# #     return mysql.connector.connect(
# #         host="localhost",
# #         user="root",
# #         password="ashu",
# #         database="owners"   # ensure property table exists here
# #     )


# # ---------------------- MODIFY PROPERTY ROUTE ----------------------
@app.route("/modify_property", methods=["GET", "POST"])
def modify_property():
    property_data = None

    if request.method == "POST":
        # ---- SEARCH ----
        if "search" in request.form:
            search_code = request.form["search_property_code"]

            conn = get_owners_db()
            cur = conn.cursor(dictionary=True)

            cur.execute("SELECT * FROM property WHERE property_code = %s", (search_code,))
            property_data = cur.fetchone()

            if property_data and property_data.get("property_photo"):
                property_data["property_photo"] = base64.b64encode(property_data["property_photo"]).decode("utf-8")

            cur.close()
            conn.close()

            if not property_data:
                flash("No property found with that code!", "danger")

        # ---- UPDATE ----
        elif "property_code" in request.form:
            try:
                conn = get_owners_db()
                cur = conn.cursor()

                property_code = request.form["property_code"]

                update_query = """
                    UPDATE property SET
                        primary_owner_code=%s,
                        developer_name=%s,
                        building_name=%s,
                        property_type=%s,
                        name=%s,
                        address1=%s,
                        address2=%s,
                        city=%s,
                        state=%s,
                        country=%s,
                        zip_code=%s,
                        municipality_number=%s,
                        electricity_bill_number=%s,
                        water_bill_number=%s,
                        ownership_type=%s,
                        furnishing_status=%s,
                        land_area=%s,
                        carpet_area=%s,
                        builtup_area=%s,
                        bedrooms=%s,
                        bathrooms=%s,
                        washrooms=%s,
                        facing=%s,
                        car_parkings=%s,
                        servant_rooms=%s,
                        balconies=%s,
                        has_dishwasher=%s,
                        has_washing_machine=%s,
                        property_value=%s,
                        year_of_construction=%s,
                        expected_rent_value=%s,
                        status=%s,
                        created_by=%s,
                        creation_date=%s,
                        property_photo=%s
                    WHERE property_code=%s
                """

                # ---- Get updated form data ----
                data = (
                    request.form.get("primary_owner_code"),
                    request.form.get("developer_name"),
                    request.form.get("building_name"),
                    request.form.get("property_type"),
                    request.form.get("name"),
                    request.form.get("address1"),
                    request.form.get("address2"),
                    request.form.get("city"),
                    request.form.get("state"),
                    request.form.get("country"),
                    request.form.get("zip_code"),
                    request.form.get("municipality_number"),
                    request.form.get("electricity_bill_number"),
                    request.form.get("water_bill_number"),
                    request.form.get("ownership_type"),
                    request.form.get("furnishing_status"),
                    request.form.get("land_area"),
                    request.form.get("carpet_area"),
                    request.form.get("builtup_area"),
                    request.form.get("bedrooms"),
                    request.form.get("bathrooms"),
                    request.form.get("washrooms"),
                    request.form.get("facing"),
                    request.form.get("car_parkings"),
                    request.form.get("servant_rooms"),
                    request.form.get("balconies"),
                    request.form.get("has_dishwasher"),
                    request.form.get("has_washing_machine"),
                    request.form.get("property_value"),
                    request.form.get("year_of_construction") or None,
                    request.form.get("expected_rent_value"),
                    request.form.get("status"),
                    request.form.get("created_by"),
                    request.form.get("creation_date") or date.today(),
                    request.files["property_photo"].read() if "property_photo" in request.files and request.files["property_photo"].filename else None,
                    property_code
                )

                cur.execute(update_query, data)
                conn.commit()

                flash("Property details updated successfully!", "success")
            except Exception as e:
                flash(f"Error updating property: {str(e)}", "danger")
            finally:
                cur.close()
                conn.close()

    return render_template("modify_property.html", property=property_data)


# from io import BytesIO

# @app.route('/property_photo/<property_code>')
# def property_photo(property_code):
#     conn = get_owners_db()
#     cursor = conn.cursor()

#     cursor.execute("SELECT property_photo FROM property WHERE property_code = %s", (property_code,))
#     photo_data = cursor.fetchone()
#     cursor.close()
#     conn.close()

#     if photo_data and photo_data[0]:
#         return send_file(BytesIO(photo_data[0]), mimetype='image/jpeg')
#     else:
#         # Return a placeholder image if none stored
#         return send_file(BytesIO(b''), mimetype='image/jpeg')
# # ---------------- DELETE PROPERTY ----------------

# # def get_owners_db():
# #     return mysql.connector.connect(
# #         host="localhost",
# #         user="root",
# #         password="ashu",
# #         database="owners"
# #     )

@app.route("/delete_property", methods=["GET", "POST"])
def delete_property():
    property_data = None

    if request.method == "POST":
        property_code = request.form.get("property_code")  # ensure you get it

        conn = get_owners_db()
        cur = conn.cursor(dictionary=True)

        if "search" in request.form:
            cur.execute("SELECT * FROM property WHERE property_code = %s", (property_code,))
            property_data = cur.fetchone()
            if property_data and property_data.get("property_photo"):
                property_data["property_photo"] = base64.b64encode(property_data["property_photo"]).decode("utf-8")
            if not property_data:
                flash("No property found with that code!", "danger")

        elif "delete" in request.form:
            try:
                cur.execute("DELETE FROM property WHERE property_code = %s", (property_code,))
                conn.commit()
                flash(f"Property {property_code} deleted successfully!", "success")
                property_data = None  # important!
            except Exception as e:
                flash(f"Error deleting property: {str(e)}", "danger")

        cur.close()
        conn.close()

    return render_template("delete_property.html", property=property_data)
# #-----------------list--------------

# # ✅ Database connection function (reuse for consistency)
# # def get_property_db():
# #     return mysql.connector.connect(
# #         host="localhost",
# #         user="root",
# #         password="ashu",
# #         database="owners"     # ← replace with your database name
# #     )

# # ✅ Route: List all properties
# @app.route("/list_property")
# def list_property():
#     try:
#         conn = get_owners_db()
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("""
#             SELECT property_code, primary_owner_code, developer_name, building_name, property_type,
#                    name, address1, address2, city, state, country, zip_code, municipality_number,
#                    electricity_bill_number, water_bill_number, ownership_type, furnishing_status,
#                    land_area, carpet_area, builtup_area, bedrooms, bathrooms, washrooms, facing,
#                    car_parkings, servant_rooms, balconies, has_dishwasher, has_washing_machine,
#                    property_value, year_of_construction, second_owner_code, expected_rent_value,
#                    status, mtd_income, ytd_income, mtd_expense, ytd_expense, purchase_value,
#                    construction_cost, renovation_cost, registration, transfer_fees, misc_expense,
#                    created_by, creation_date, property_photo
#             FROM property
#         """)
#         properties = cursor.fetchall()

#         # Convert BLOB to Base64 for displaying images
#         for prop in properties:
#             if prop["property_photo"]:
#                 prop["property_photo"] = base64.b64encode(prop["property_photo"]).decode('utf-8')

#         return render_template("list_property.html", properties=properties)

#     except mysql.connector.Error as err:
#         return f"Database Error: {err}"

#     finally:
#         if conn.is_connected():
#             cursor.close()
#             conn.close()
# # ---------------- ADD TENANT ROUTE ----------------
# # from flask import g

# # def get_db():
# #     if "db" not in g:
# #         g.db = mysql.connector.connect(
# #             host="localhost", user="root", password="ashu", database="owners"
# #         )
# #     return g.db

# # @app.teardown_appcontext
# # def close_db(exception):
# #     db = g.pop("db", None)
# #     if db is not None:
# #         db.close()

# from werkzeug.utils import secure_filename
# # from werkzeug.security import generate_password_hash, check_password_hash

# # # During registration
# # hashed = generate_password_hash(password)

# # # During login
# # check_password_hash(user["Password"], password)

# # def get_connection():
# #     return mysql.connector.connect(
# #         host="localhost",
# #         user="root",
# #         password="ashu",
# #         database="owners"
# #     )



# @app.route("/add_tenant", methods=["GET", "POST"])
# def add_tenant():
#     if request.method == "POST":
#         try:
#             conn = get_owners_db()
#             cursor = conn.cursor()

#             # Read uploaded files as binary
#             def read_file(field_name):
#                 file = request.files.get(field_name)
#                 if file and file.filename:
#                     return file.read()  # read binary
#                 return None

#             data = (
#                 request.form.get("tenant_name"),
#                 request.form.get("tenant_dob"),
#                 request.form.get("tenant_nationality"),
#                 request.form.get("tenant_passport_number"),
#                 request.form.get("tenant_emirates_id"),
#                 request.form.get("tenant_passport_expiry"),
#                 request.form.get("tenant_eid_expiry"),
#                 request.form.get("tenant_employer"),
#                 request.form.get("tenant_mobile"),
#                 request.form.get("tenant_email"),
#                 request.form.get("lease_start"),
#                 request.form.get("lease_end"),
#                 request.form.get("move_in"),
#                 request.form.get("move_out"),
#                 request.form.get("rent_amount"),
#                 request.form.get("deposit_amount"),
#                 request.form.get("number_of_payments"),
#                 read_file("passportcopypath"),
#                 read_file("eidcopypath"),
#                 read_file("residencevisacopypath"),
#                 read_file("bankstatementcopypath"),
#                 read_file("depositchequecopypath"),
#                 read_file("securitychequecopypath"),
#                 read_file("ejarimunicipalregistrationcopypath"),
#                 request.form.get("created_by"),
#                 request.form.get("creation_date")
#             )

#             insert_query = """
#                 INSERT INTO TenancyContracts (
#                     TenantName, TenantDOB, TenantNationality,
#                     TenantPassportNumber, TenantEmiratesID,
#                     TenantPassportExpiryDate, TenantEIDExpiryDate,
#                     TenantEmployer, TenantMobileNumber, TenantEmailID,
#                     LeaseStartDate, LeaseEndDate, MoveInDate, MoveOutDate,
#                     RentAmount, DepositAmountReceived, NumberOfPayments,
#                     PassportCopyPath, EIDCopyPath, ResidenceVisaCopyPath,
#                     BankStatementCopyPath, DepositChequeCopyPath,
#                     SecurityChequeCopyPath, EjariMunicipalRegistrationCopyPath,
#                     CreatedBy, CreationDate
#                 ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#             """

#             cursor.execute(insert_query, data)
#             conn.commit()
#             new_id = cursor.lastrowid
#             flash(f"Tenant added successfully! Tenancy Contract Number: {new_id}", "success")

#         except Error as e:
#             flash(f"Database Error: {e}", "error")
#         finally:
#             if conn.is_connected():
#                 cursor.close()
#                 conn.close()

#         return redirect(url_for("add_tenant"))

#     today = date.today().strftime("%Y-%m-%d")
#     return render_template("add_tenant.html", today=today)
# # from flask import send_file, abort

# # ------------------ Tenant Modify ------------------
# # import base64
# # def get_db_connection():
# #     return mysql.connector.connect(
# #         host="localhost",
# #         user="root",
# #         password="ashu",  # your MySQL password
# #         database="owners"
# #     )
# # Serve tenant images
# @app.route("/tenant_image/<int:tenant_id>/<file_type>")
# def tenant_image(tenant_id, file_type):
#     conn = get_owners_db()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("""
#         SELECT PassportCopyPath, EIDCopyPath, ResidenceVisaCopyPath,
#                BankStatementCopyPath, DepositChequeCopyPath,
#                SecurityChequeCopyPath, EjariMunicipalRegistrationCopyPath
#         FROM TenancyContracts WHERE TenancyContractNumber=%s
#     """, (tenant_id,))
#     tenant = cursor.fetchone()
#     cursor.close()
#     conn.close()

#     mapping = {
#         "PassportCopyPath": "PassportCopyPath",
#         "EIDCopyPath": "EIDCopyPath",
#         "ResidenceVisaCopyPath": "ResidenceVisaCopyPath",
#         "BankStatementCopyPath": "BankStatementCopyPath",
#         "DepositChequeCopyPath": "DepositChequeCopyPath",
#         "SecurityChequeCopyPath": "SecurityChequeCopyPath",
#         "EjariMunicipalRegistrationCopyPath": "EjariMunicipalRegistrationCopyPath"
#     }

#     if tenant and file_type in mapping and tenant[mapping[file_type]]:
#         return tenant[mapping[file_type]], 200, {"Content-Type": "image/jpeg"}
#     else:
#         return redirect(url_for('static', filename='no_image.png'))

@app.route("/modify_tenant", methods=["GET", "POST"])
def modify_tenant():
    tenant = None
    today = date.today()

    if request.method == "POST":
        conn = get_owners_db()
        cursor = conn.cursor(dictionary=True)

        if "search" in request.form:
            contract_number = request.form.get("tenancyContractNumber")
            cursor.execute("SELECT * FROM TenancyContracts WHERE TenancyContractNumber=%s", (contract_number,))
            tenant = cursor.fetchone()
            if tenant:
                for field in ["PassportCopyPath","EIDCopyPath","ResidenceVisaCopyPath",
                              "BankStatementCopyPath","DepositChequeCopyPath","SecurityChequeCopyPath",
                              "EjariMunicipalRegistrationCopyPath"]:
                    if tenant[field]:
                        tenant[field] = base64.b64encode(tenant[field]).decode("utf-8")
            else:
                flash(f"No tenant found with Contract Number: {contract_number}", "error")

        # ----- UPDATE TENANT -----
        elif "update_tenant" in request.form:
            contract_number = request.form.get("tenancy_contract_number")
            # Collect form data
            data_fields = [
                "tenant_name","tenant_dob","tenant_nationality","tenant_passport","tenant_eid",
                "passport_expiry","eid_expiry","tenant_employer","tenant_mobile","tenant_email",
                "lease_start","lease_end","move_in","move_out","rent_amount",
                "deposit_amount","number_of_payments","created_by","creation_date"
            ]
            data = [request.form.get(f) for f in data_fields]

            # Update main fields
            update_query = f"""
                UPDATE TenancyContracts SET
                TenantName=%s, TenantDOB=%s, TenantNationality=%s,
                TenantPassportNumber=%s, TenantEmiratesID=%s, TenantPassportExpiryDate=%s,
                TenantEIDExpiryDate=%s, TenantEmployer=%s, TenantMobileNumber=%s, TenantEmailID=%s,
                LeaseStartDate=%s, LeaseEndDate=%s, MoveInDate=%s, MoveOutDate=%s,
                RentAmount=%s, DepositAmountReceived=%s, NumberOfPayments=%s,
                CreatedBy=%s, CreationDate=%s
                WHERE TenancyContractNumber=%s
            """
            cursor.execute(update_query, data + [contract_number])

            # Update uploaded files
            file_fields = ["PassportCopyPath","EIDCopyPath","ResidenceVisaCopyPath",
                           "BankStatementCopyPath","DepositChequeCopyPath","SecurityChequeCopyPath",
                           "EjariMunicipalRegistrationCopyPath"]
            for field in file_fields:
                file = request.files.get(field)
                if file and file.filename:
                    cursor.execute(f"UPDATE TenancyContracts SET {field}=%s WHERE TenancyContractNumber=%s",
                                   (file.read(), contract_number))

            conn.commit()
            cursor.close()
            conn.close()

            # Redirect to same page to show popup
            flash(f"✅ Tenant details updated successfully for Tenant ID : {contract_number}", "success")
            return redirect(url_for("modify_tenant"))

    return render_template("modify_tenant.html", tenant=tenant, today=today)
# # ---------------- TENANT DELETE ROUTE ----------------
@app.route("/tenant_delete", methods=["GET", "POST"])
def tenant_delete():
    tenant = None

    if request.method == "POST":
        conn = get_owners_db()
        cursor = conn.cursor(dictionary=True)

        contract_number = request.form.get("tenancyContractNumber")

        # ----- SEARCH TENANT -----
        if "search" in request.form:
            cursor.execute("SELECT * FROM TenancyContracts WHERE TenancyContractNumber=%s", (contract_number,))
            tenant = cursor.fetchone()
            if tenant:
                file_fields = [
                    "PassportCopyPath", "EIDCopyPath", "ResidenceVisaCopyPath",
                    "BankStatementCopyPath", "DepositChequeCopyPath",
                    "SecurityChequeCopyPath", "EjariMunicipalRegistrationCopyPath"
                ]
                for field in file_fields:
                    if tenant[field]:
                        tenant[field] = base64.b64encode(tenant[field]).decode("utf-8")
            else:
                flash(f"No tenant found with Contract Number: {contract_number}")

        # ----- DELETE TENANT -----
        elif "delete_tenant" in request.form:
            cursor.execute("DELETE FROM TenancyContracts WHERE TenancyContractNumber=%s", (contract_number,))
            conn.commit()
            flash(f"✅ Tenant successfully deleted for Contract Number: {contract_number}")
            tenant = None  # Clear tenant after deletion

        cursor.close()
        conn.close()

    return render_template("tenant_delete.html", tenant=tenant)
#     #-------------------list tanant
# # import base64

@app.route("/tenant_list")
def tenant_list():
    conn = get_owners_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM TenancyContracts ORDER BY TenancyContractNumber DESC")
    tenants = cursor.fetchall()

    # Convert LONGBLOB fields to base64
    file_fields = [
        "PassportCopyPath","EIDCopyPath","ResidenceVisaCopyPath",
        "BankStatementCopyPath","DepositChequeCopyPath",
        "SecurityChequeCopyPath","EjariMunicipalRegistrationCopyPath"
    ]
    for tenant in tenants:
        for field in file_fields:
            if tenant[field]:
                tenant[field] = base64.b64encode(tenant[field]).decode("utf-8")

    cursor.close()
    conn.close()
    return render_template("tenant_list.html", tenants=tenants)


# UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")  # Folder in your project directory
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route("/uploads/<filename>")
# def uploaded_file(filename):
#     return send_from_directory(app.config["UPLOAD_FOLDER"], filename)



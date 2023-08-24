from flask import *
import pymysql

# start
app = Flask(__name__)
# SESSIONS
# step 1: Provide secret key to your application
# Avoid session hijacking, cross -site scripting
app.secret_key = "1234#$fuhutguhiknknnnnk6568gghcghhvufuy"

# 1. Vendor Registration


@app.route('/vendor_registration', methods=['POST', 'GET'])
def register_vendor():
   if request.method == 'POST':
       vendor_name = request.form['name']
       vendor_contact = request.form['contact']
       vendor_email = request.form['email']
       vendor_location = request.form['location']
       vendor_password = request.form['password']

       vendor_photo = request.files['photo']
       vendor_photo.save('static/images/' + vendor_photo.filename)

       vendor_desc = request.form['desc']

       connection = pymysql.connect(
           host='localhost', user='root', password='', database='dshopdb')

       cursor = connection.cursor()

       data = (vendor_name, vendor_contact, vendor_email,
               vendor_location, vendor_password, vendor_photo.filename, vendor_desc)

       sql = "insert into vendors (vendor_name, vendor_contact, vendor_email, vendor_location,vendor_password, vendor_photo, vendor_desc) values (%s, %s, %s, %s, %s, %s, %s)"

       cursor.execute(sql, data)
       connection.commit()

       return render_template('vendor_register.html', message='Vendor Registred Successful')

   else:
       return render_template('vendor_register.html', message='Please Register Here')
   

@app.route('/vendor_login', methods=['POST', 'GET'])
def vendor_login():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']

        connection = pymysql.connect(
            host='localhost', user='root', password='', database='dshopdb')

        cursor = connection.cursor()

        sql = 'select * from vendors where vendor_name = %s and vendor_password = %s'
        data = (username, password)
        cursor.execute(sql, data)

        count = cursor.rowcount
        if count == 0:
            return render_template('vendor_login.html', message='Invalid Credentials')
        else:
            # session: Store Information About a specific user
            user_record = cursor.fetchone()
            session['key'] = user_record[1]
            session['vendor_id'] = user_record[0]
            session['contact'] = user_record[2]
            session['location'] = user_record[4]
            session['image'] = user_record[5]
            # session['desc'] = user_record[7]

            return redirect('/vendor_profile')
    else:
        return render_template('vendor_login.html', message='Please Login Here')
    

@app.route('/vendor_profile')
def vendor_profile():
    return render_template('vendor_profile.html')


app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
import scraper
from sqlalchemy.sql import func

def create_database(app) : 
    with app.app_context():
        if not path.exists(path.join(app.instance_path, DB_NAME)):
            db.create_all()
            print('Database created')

db = SQLAlchemy()
DB_NAME = "database.db"

class Entry (db.Model) :

    l2Id = db.Column(db.String(8), primary_key = True)
    PID = db.Column(db.String(11))
    prod_name = db.Column(db.String(80))
    prod_color = db.Column(db.String(30))
    prod_size = db.Column(db.String(10))
    prod_status = db.Column(db.String(15))
    prod_curr_price = db.Column(db.String(8))
    prod_max_price = db.Column(db.String(8))
    prod_min_price = db.Column(db.String(8))
    url = db.Column(db.String(300))
    date = db.Column(db.DateTime(timezone=True), default = func.now())

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
db.init_app(app)

create_database(app)

with app.app_context() :
    db.create_all()

#homepage containing tracked table
@app.route('/', methods =['POST', 'GET'])
def index() :
    entries = Entry.query.all()
    
    pid_set = set()
    for entry in entries : 
        pid_set.add(entry.PID)
    pid_list = list(pid_set)

    return render_template('index.html', entries=entries, pid_list = pid_list)

#page to display scraped data
@app.route('/table', methods=['POST','GET'])
def show_table() : 
    if request.method == 'POST' :

        #make variables being passed to table.html above so no error
        size_tuple = tuple()
        result = list()
        main_url = ''

        #sale group variables returned
        sale_group_exists_01 = False
        sale_group_size_tuple_01 = tuple()
        sale_group_result_01 = list()
        sale_url_01 = ''

        sale_group_exists_02 = False
        sale_group_size_tuple_02 = tuple()
        sale_group_result_02 = list()
        sale_url_02 = ''

        try: 
            PID = request.form.get('input_PID')
            
            #general info for non-sale group
            prod_name = scraper.product_name(PID)
            size_list = []
            size_list = scraper.get_size_list(PID, '00')
            size_tuple = scraper.get_sizes(size_list)
            result = scraper.product_info(PID,'00')
            main_url = 'https://www.uniqlo.com/us/en/products/' + PID + '/00'

            #sale group 01 info
            sale_group_exists_01 = scraper.sale_group_exist(PID, '01')
            if sale_group_exists_01 :
                sale_group_size_list_01 = scraper.get_size_list(PID, '01')
                sale_group_size_tuple_01 = scraper.get_sizes(sale_group_size_list_01)
                sale_group_result_01 = scraper.product_info(PID,'01')
                sale_url_01 = 'https://www.uniqlo.com/us/en/products/' + PID + '/01'

            #sale group 02 info
            sale_group_exists_02 = scraper.sale_group_exist(PID, '02')
            if sale_group_exists_02 :
                sale_group_size_list_02 = scraper.get_size_list(PID, '02')
                sale_group_size_tuple_02 = scraper.get_sizes(sale_group_size_list_02)
                sale_group_result_02 = scraper.product_info(PID,'02')
                sale_url_02 = 'https://www.uniqlo.com/us/en/products/' + PID + '/02'    
        except: 
            IndexError
            prod_name = "Invalid Product ID"
    
    return render_template('table.html',
                           PID = PID, 
                           prod_name = prod_name, 
                           size_tuple = size_tuple, 
                           result = result, 
                           sale_group_exists_01 = sale_group_exists_01, 
                           sale_group_size_tuple_01 = sale_group_size_tuple_01, 
                           sale_group_result_01 = sale_group_result_01, 
                           sale_group_exists_02 = sale_group_exists_02, 
                           sale_group_size_tuple_02 = sale_group_size_tuple_02, 
                           sale_group_result_02 = sale_group_result_02, 
                           main_url = main_url, 
                           sale_url_01 = sale_url_01,
                           sale_url_02 = sale_url_02,
                           db = db,
                           Entry = Entry
                           )

@app.route('/add_items', methods=['POST'])
def add_items() : 
    #needs a way to handle duplicates l2id's
    item_ids = request.form.getlist('items')
    for items in item_ids : 
        p_l2id = request.form.get(f'p_l2id_{items}')
        p_id = items[:11]
        p_name = request.form.get(f'p_name_{items}')
        p_color = request.form.get(f'p_color_{items}')
        p_size = request.form.get(f'p_size_{items}')
        p_status = request.form.get(f'p_status_{items}')
        p_curr_price = request.form.get(f'p_curr_price_{items}')
        p_url = request.form.get(f'p_link_{items}')
        
        new_entry = Entry(l2Id = p_l2id,
                        PID = p_id, 
                        prod_name = p_name, 
                        prod_color = p_color, 
                        prod_size = p_size,
                        prod_status = p_status,
                        prod_curr_price = p_curr_price,
                        prod_max_price = '0',
                        prod_min_price = '0',
                        url = p_url
                        )
        db.session.add(new_entry)
        db.session.commit()
        print(f"ADDED: {p_name} | {p_color} | {p_size} = ({p_status}, {p_curr_price})")
        
        
    return redirect(url_for('index'))

@app.route('/remove', methods = ['POST'])
def remove() : 
    l2Id_to_remove = request.form.get('remove')
    entry_to_remove = db.session.get(Entry, l2Id_to_remove)
    
    prod_name_to_remove = request.form.get('remove_name')
    prod_color_to_remove = request.form.get('remove_color')
    prod_size_to_remove = request.form.get('remove_size')

    db.session.delete(entry_to_remove)
    db.session.commit()
    print(f"REMOVED: {prod_name_to_remove} | color: {prod_color_to_remove} | size: {prod_size_to_remove}")

    return redirect(url_for('index'))

@app.route('/update_all', methods = ['POST', 'GET'])
def update_all() : 
    entry_list = db.session.query(Entry).all()
    for entry in entry_list : 
        #need PID + l2Id + group to update -> get the group from url column
        prod_name = entry.prod_name
        prod_color = entry.prod_color
        prod_size = entry.prod_size
        prod_PID = entry.PID
        prod_l2Id = entry.l2Id
        prod_group = entry.url[-2:] #last 2 digits in URL = group

        #get the updated stock and price now
        updated_info = scraper.update_by_l2Id(prod_l2Id, prod_PID, prod_group)
        updated_prod_status = updated_info[0]
        updated_curr_price = updated_info[1]

        #doing the check first before updating entry
        if entry.prod_status != updated_prod_status or entry.prod_curr_price != updated_curr_price:
            scraper.send_notif(entry, updated_prod_status, updated_curr_price)

        entry.prod_status = updated_info[0]
        entry.prod_curr_price = updated_info[1]

        db.session.commit()
        print(f"UPDATE: {prod_name} | {prod_color} | {prod_size} = {updated_info}" )

    return redirect(url_for('index'))


if __name__ == "__main__" :
    scraper.get_target_email()
    app.run()
from flask import Flask, render_template, request, redirect, url_for, flash
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
    img_link = db.Column(db.String(300))
    sale_status = db.Column(db.String(8)) #scraper fnuction returns bool but this stored as string
    url = db.Column(db.String(300))
    date = db.Column(db.DateTime(timezone=True), default = func.now())

app = Flask(__name__)
app.secret_key = "Uniqlo"
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
    img_dict = dict()
    for entry in entries : 
        pid_set.add(entry.PID)
        img_dict.update({entry.PID : entry.img_link})
    pid_list = list(pid_set)
    
    return render_template('index.html', entries=entries, pid_list = pid_list, img_dict = img_dict)

#page to display scraped data
@app.route('/table', methods=['POST','GET'])
def show_table() : 
    if request.method == 'POST' :

        #make variables being passed to table.html above so no error
        size_tuple = tuple()
        result = list()
        main_url = ''
        sale_status = False
        img_link = 'https://static-00.iconduck.com/assets.00/unavailable-icon-2048x2048-eyjkqwgr.png'

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
            sale_status = scraper.product_sale_status(PID)
            img_link = scraper.product_img(PID)

            #sale group 01 info
            sale_group_exists_01 = scraper.sale_group_exist(PID, '01')
            if sale_group_exists_01 :
                sale_group_size_list_01 = scraper.get_size_list(PID, '01')
                sale_group_size_tuple_01 = scraper.get_sizes(sale_group_size_list_01)
                sale_group_result_01 = scraper.product_info(PID,'01')
                sale_url_01 = 'https://www.uniqlo.com/us/en/products/' + PID + '/01'
                img_link = scraper.product_img(PID)

            #sale group 02 info
            sale_group_exists_02 = scraper.sale_group_exist(PID, '02')
            if sale_group_exists_02 :
                sale_group_size_list_02 = scraper.get_size_list(PID, '02')
                sale_group_size_tuple_02 = scraper.get_sizes(sale_group_size_list_02)
                sale_group_result_02 = scraper.product_info(PID,'02')
                sale_url_02 = 'https://www.uniqlo.com/us/en/products/' + PID + '/02' 
                img_link = scraper.product_img(PID)   
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
                           sale_status = sale_status,
                           img_link = img_link,
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
        p_img_link = request.form.get(f'p_img_link_{items}')
        p_sale_status = request.form.get(f'p_sale_status_{items}')
        p_url = request.form.get(f'p_link_{items}')
        
        new_entry = Entry(l2Id = p_l2id,
                        PID = p_id, 
                        prod_name = p_name, 
                        prod_color = p_color, 
                        prod_size = p_size,
                        prod_status = p_status,
                        prod_curr_price = p_curr_price,
                        img_link = p_img_link,
                        sale_status = p_sale_status,
                        url = p_url
                        )
        db.session.add(new_entry)
        db.session.commit()
        print(f"ADDED: {p_name} | {p_color} | sale = {p_sale_status} | {p_size} = ({p_status}, {p_curr_price})")
        
        
    return redirect(url_for('index'))

@app.route('/remove', methods = ['POST'])
def remove() : 
    l2Id_to_remove = request.form.get('remove')
    entry_to_remove = db.session.get(Entry, l2Id_to_remove)
    
    prod_name_to_remove = request.form.get('remove_name')
    prod_color_to_remove = request.form.get('remove_color')
    prod_status_to_remove = request.form.get('remove_status')
    prod_size_to_remove = request.form.get('remove_size')

    db.session.delete(entry_to_remove)
    db.session.commit()
    print(f"REMOVED: {prod_name_to_remove} | {prod_color_to_remove} | sale = {prod_status_to_remove} | size = {prod_size_to_remove}")

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

        #UPDATE sale status -> depends on group, scraper function only works for group 00
        if prod_group == '00' :
            updated_sale_status = str(scraper.product_sale_status(prod_PID))
        elif prod_group == '01' or prod_group == '02' :
            updated_sale_status = 'True'

        # MESSAGE FLASHING) if change detected flash message for (name, color, size -> change detected) 

        #green = price drop / sale change from False to True / stock change to 'in stock'
        if float(updated_curr_price[1:]) < float(entry.prod_curr_price[1:]) : 
            flash(f"{prod_name} | Size: ({prod_size}) | Col: ({prod_color}) | PRICE UPDATE = {entry.prod_curr_price} -> {updated_curr_price}", 'green')
        if updated_sale_status == 'True' and entry.sale_status != 'True' :
            flash(f"{prod_name} | Size: ({prod_size}) | Col: ({prod_color}) | SALE UPDATE = {entry.prod_curr_price} -> {updated_curr_price}", 'green')
        if updated_prod_status == 'In stock' and entry.prod_status != 'In stock' : 
            flash(f"{prod_name} | Size: ({prod_size}) | Col: ({prod_color}) | STOCK UPDATE = {entry.prod_status} -> {updated_prod_status}", 'green')
        
        #yellow = stock change to 'low stock' 
        if updated_prod_status == 'Low stock' and entry.prod_status != 'Low stock' :
            flash(f"{prod_name} | Size: ({prod_size}) | Col: ({prod_color}) | STOCK UPDATE = {entry.prod_status} -> {updated_prod_status}", 'yellow')
        
        #red = price increase / sale change from True to False / stock change to 'out of stock'
        if float(updated_curr_price[1:]) > float(entry.prod_curr_price[1:]) : 
            flash(f"{prod_name} | Size: ({prod_size}) | Col: ({prod_color}) | PRICE UPDATE = {entry.prod_curr_price} -> {updated_curr_price}", 'red')
        if updated_sale_status == 'False' and entry.sale_status != 'False' :
            flash(f"{prod_name} | Size: ({prod_size}) | Col: ({prod_color}) | SALE UPDATE = {entry.prod_curr_price} -> {updated_curr_price}", 'red')
        if updated_prod_status == 'Out of stock' and entry.prod_status != 'Out of stock' : 
            flash(f"{prod_name} | Size: ({prod_size}) | Col: ({prod_color}) | STOCK UPDATE = {entry.prod_status} -> {updated_prod_status}", 'red')

        entry.prod_status = updated_info[0]
        entry.prod_curr_price = updated_info[1]
        entry.sale_status = updated_sale_status

        db.session.commit()
        print(f"UPDATE: {prod_name} | {prod_color} | sale = {updated_sale_status} | {prod_size} = {updated_info}" )

    return redirect(url_for('index'))


if __name__ == "__main__" :
    app.run()
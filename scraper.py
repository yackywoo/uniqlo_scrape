from bs4 import BeautifulSoup
import requests
import time

def product_name(PID) :
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.uniqlo.com/us/en/products/' + PID + '/',
        'DNT': '1',
        'Sec-GPC': '1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Connection': 'keep-alive',
        'Priority': 'u=4',
    } 
    url = 'https://www.uniqlo.com/us/api/commerce/v5/en/products?productIds=' + PID
    response = requests.get(url, headers=headers)
    response = response.json()

    try:
        #THE API call above returns empty JSON when clothes go completely O.O.S
        #no way of getting the product name 
        #can get name thru reviews but if no reviews then no prod. name either
        name = response['result']['items'][0]['name'] 
    except: 
        IndexError
        name = "Out of Stock"

    return name

def product_sale_status(PID) : 
    #get sale status
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.uniqlo.com/us/en/products/' + PID + '/',
        'DNT': '1',
        'Sec-GPC': '1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Connection': 'keep-alive',
        'Priority': 'u=4',
    } 
    url = 'https://www.uniqlo.com/us/api/commerce/v5/en/products?productIds=' + PID
    response = requests.get(url, headers=headers)
    response = response.json()

    try: 
        sale_status = response['result']['items'][0]['prices']['promo']
    except: 
        #index error occurs when OOS. so return false by default
        IndexError
        return False

    if sale_status != None : 
        #if promo section exists then sale exists and RETURN TRUE else FALSE
        return True
    else :
        return False

def product_img(PID) : 
    #get the first product img
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.uniqlo.com/us/en/products/' + PID + '/',
        'DNT': '1',
        'Sec-GPC': '1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Connection': 'keep-alive',
        'Priority': 'u=4',
    } 
    url = 'https://www.uniqlo.com/us/api/commerce/v5/en/products?productIds=' + PID
    response = requests.get(url, headers=headers)
    response = response.json()

    try: 
        colors = response['result']['items'][0]['images']['main']
        color_list = list(colors)
        first_color = color_list[0]
        img_link = colors[first_color]['image']
    except:
        IndexError
        img_link = 'https://static-00.iconduck.com/assets.00/unavailable-icon-2048x2048-eyjkqwgr.png'

    return img_link

def product_info(PID, group) :
    color_dict = {
        '00' : 'WHITE',
        '01' : 'OFF-WHITE',
        '02' : 'LIGHT GRAY',
        '03' : 'LIGHT GRAY',
        '08' : 'DARK GRAY',
        '07' : 'GRAY',
        '09' : 'BLACK',
        '15' : 'RED',
        '33' : 'KHAKI',
        '36' : 'BROWN',
        '52' : 'LIGHT GREEN',
        '55' : 'DARK GREEN',
        '67' : 'BLUE',
        '69' : 'NAVY',
        '71' : 'LIGHT PURPLE',
        '76' : 'DARK PURPLE',
        '34' : 'BROWN',
        '38' : 'DARK BROWN',
        '66' : 'BLUE',
        '32' : 'BIEGE',
        '31' : 'BIEGE',
        '35' : 'BROWN',
        '30' : 'NATURAL',
        '99' : 'OTHER',
        '56' : 'OLIVE',
        '68' : 'BLUE',
        '11' : 'PINK',
        '10' : 'PINK', 
        '64' : 'BLUE',
        '72' : 'PURPLE',
        '58' : 'DARK GREEN',
        '000' : 'BLANK',

    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.uniqlo.com/us/en/products/' + PID + '/',
        'DNT': '1',
        'Sec-GPC': '1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Connection': 'keep-alive',
        'Priority': 'u=4',
    } 
    url = 'https://www.uniqlo.com/us/api/commerce/v5/en/products/' + PID + '/price-groups/' + group + '/l2s?alterationId=40&withPrices=true&withStocks=true&includePreviousPrice=false&httpFailure=true'
    response = requests.get(url, headers=headers)
    response = response.json()

    avail_colors = set() #num of columns
    avail_sizes = set() #num of rows
    avail_codes = dict() #{commCode : l2Id} pairs for later
    size_list = list()

    #store the raw codes of colors and sizes
    for l2s in response['result']['l2s'] : 
        avail_colors.add(l2s['color']['displayCode'])
        avail_sizes.add(l2s['size']['displayCode'])
        size_list.append(l2s['size']['displayCode'])

        #generate key because some of thbe PID's aren't consistent in uniqlo's API
        key = f"{PID[1:7]}-{l2s['color']['displayCode']}-{l2s['size']['displayCode']}-000"
        avail_codes.update({key : l2s['l2Id']})

    #making 2D communicationCode table to help map l2 ID's to later
    #sorted by color then size for the PID, grouped by color as well
    code_matrix = [[(PID[1:7] + '-' + color + '-' + size + '-000') for size in sorted(avail_sizes)] for color in sorted(avail_colors)]
    
   
    l2_matrix = list()
    
    for each_color in code_matrix :
        temp = []
        for comm_code in each_color : 
            if comm_code in list(avail_codes.keys()) :  
                temp.append(avail_codes[comm_code])  
        l2_matrix.append(temp)
    
    l2_stock_price = dict()
    
    #convert size_list from codes into english
    size_list = list(get_sizes(size_list))

    #map the l2 ID's to the stock and prices
    for l2id, sizes in zip(response['result']['stocks'], size_list) :
        #add all stock and price info as pair for the l2Id
        stock_status = response['result']['stocks'][l2id]['statusLocalized']
        curr_price = response['result']['prices'][l2id]['base']['value']
        curr_price = "$" + format(curr_price, '.2f')
        
        
        if response['result']['prices'][l2id]['promo'] == 'null' or response['result']['prices'][l2id]['promo'] == None :
            #if no sale
            sale_status = False
        else :
            sale_status = True 
        #print(f"{l2id}: {response['result']['prices'][l2id]['promo']} | sale : {sale_status}")
        l2_stock_price.update({l2id : [sizes ,stock_status, curr_price, sale_status]})

    l2_size = list()
    l2_stock = list()
    l2_price = list()
    l2_sale = list()
    l2id_list = list()

    #group size, stock and price based on color
    for each_color in l2_matrix : 
        size_temp = []
        stock_temp = []
        price_temp = []
        sale_temp = []
        l2id_temp = []
        for l2Id in each_color :
            size_temp.append(l2_stock_price[l2Id][0]) 
            stock_temp.append(l2_stock_price[l2Id][1])
            price_temp.append(l2_stock_price[l2Id][2])
            sale_temp.append(l2_stock_price[l2Id][3])
            l2id_temp.append(l2Id)
        l2_size.append(size_temp)
        l2_stock.append(stock_temp)
        l2_price.append(price_temp)
        l2_sale.append(sale_temp)
        l2id_list.append(l2id_temp)

    #converting available color codes into english 
    color_list = []
    
    for colors in sorted(avail_colors) :
        #not all colors are in color_dict
        if colors in color_dict : 
            color_list.append(color_dict[colors])
        else : 
            color_list.append(colors)

    #stock_price groups each color by their stock,price combination (positionally)
    stock_price = list()
    for sizes, stocks, prices, sales, l2ids in zip(l2_size, l2_stock, l2_price, l2_sale, l2id_list):
        temp = list()
        for size, stock, price, sale, l2id in zip(sizes, stocks, prices, sales, l2ids) : 
            temp.append([size, stock, price, sale, l2id])
        stock_price.append(temp)
    
    #result = list of pairs containing (color, [size,stock,price,sale,l2id]) -> for all available sizes)
    result = [(color, stock_price_list) for color, stock_price_list in zip(color_list, stock_price)]


    real_result = list()
    size_list = get_size_list(PID, group)
    size_tuple = get_sizes(size_list)
    for color, availabilities in result :
                #create skeleton for every size 
                availability_dict = {size: {'status': 'N/A', 'price': '', 'sale': '','l2id': ''} for size in size_tuple}
                for size, status, price, sale, l2id in availabilities : 
                    availability_dict[size] = {'status': status, 'price': price, 'sale': sale, 'l2id': l2id}
                real_result.append((color, availability_dict))

    return real_result

def get_size_list(PID, group) : 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.uniqlo.com/us/en/products/' + PID + '/',
        'DNT': '1',
        'Sec-GPC': '1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Connection': 'keep-alive',
        'Priority': 'u=4',
    } 
    url = 'https://www.uniqlo.com/us/api/commerce/v5/en/products/' + PID + '/price-groups/' + group + '/l2s?alterationId=40&withPrices=true&withStocks=true&includePreviousPrice=false&httpFailure=true'
    response = requests.get(url, headers=headers)
    response = response.json()

    size_set = set()

    for l2s in response['result']['l2s'] :
        size_set.add(l2s['size']['displayCode'])
    
    return sorted(list(size_set))

def get_sizes(list_size) : 
    size_dict = {
        '001' : 'XXS',
        '002' : 'XS',
        '003' : 'S',
        '004' : 'M',
        '005' : 'L',
        '006' : 'XL',
        '007' : 'XXL',
        '008' : '3XL',
        '017' : '17 inch',
        '018' : '18 inch',
        '019' : '19 inch',
        '020' : '20 inch',
        '021' : '21 inch',
        '022' : '22 inch',
        '023' : '23 inch',
        '024' : '24 inch',
        '025' : '25 inch',
        '026' : '26 inch',
        '027' : '27 inch',
        '028' : '28 inch',
        '029' : '29 inch',
        '030' : '30 inch',
        '031' : '31 inch',
        '032' : '32 inch',
        '033' : '33 inch',
        '034' : '34 inch',
        '035' : '35 inch',
        '036' : '36 inch',
        '037' : '37 inch',
        '038' : '38 inch',
        '039' : '39 inch',
        '040' : '40 inch',
        '041' : '41 inch',
        '042' : '42 inch',
        '043' : '43 inch', 
    }

    available_sizes = tuple( size_dict.get(size, 'One Size') for size in list_size)
    
    return available_sizes

def sale_group_exist(PID, group) :
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.uniqlo.com/us/en/products/' + PID + '/',
        'DNT': '1',
        'Sec-GPC': '1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Connection': 'keep-alive',
        'Priority': 'u=4',
    } 
    url = 'https://www.uniqlo.com/us/api/commerce/v5/en/products/' + PID + '/price-groups/' + group + '/l2s?alterationId=40&withPrices=true&withStocks=true&includePreviousPrice=false&httpFailure=true'
    response = requests.get(url, headers=headers)
    response = response.json()

    #try to get group 01's first l2id if it exists
    try : 
        group1_l2 = response['result']['l2s'][0]['l2Id'] 
    except KeyError:
        group1_l2 = ""
    
    return (group1_l2 != "")

def update_by_l2Id(l2Id, PID, group) :
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.uniqlo.com/us/en/products/' + PID + '/',
        'DNT': '1',
        'Sec-GPC': '1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Connection': 'keep-alive',
        'Priority': 'u=4',
    } 
    url = 'https://www.uniqlo.com/us/api/commerce/v5/en/products/' + PID + '/price-groups/' + group + '/l2s?alterationId=40&withPrices=true&withStocks=true&includePreviousPrice=false&httpFailure=true'
    response = requests.get(url, headers=headers)
    response = response.json()

    try: 
        updated_stock_status = response['result']['stocks'][l2Id]['statusLocalized']
    except:
        IndexError
        updated_stock_status = "Out of stock"

    try: 
        updated_price = response['result']['prices'][l2Id]['base']['value']
        updated_price = '$' + format(updated_price, '.2f')
    except:
        IndexError
        updated_price = ''

    return (updated_stock_status, updated_price)

''' (not going to use email notifs anymore)
def get_target_email() : 
    file = open("target_email.txt", "r")

    if file.read() == '' : 
        target_email = input("Enter your email to recieve notifications: ").strip()
        
        confirm = input(f"Confirm email: {target_email}\n[Y/N]: ").strip()
        
        if confirm == 'Y' or confirm == 'y':
            print(f"{target_email} has been confirmed.")
            file = open("target_email.txt", "w")
            file.write(target_email)
            file.close()
        else : 
            get_target_email()

def send_notif(entry, updated_status, updated_price) :
    file = open("target_email.txt", "r")
    target_email = file.read()
    file.close()

    from email_notif import sender_email, sender_pass
    import smtplib
    subject = f"Update for: {entry.prod_name} {entry.prod_color} {entry.prod_size}"
    message = f"""
    Stock status has gone from: {entry.prod_status} to {updated_status}.
    Price has gone from: {entry.prod_curr_price} to {updated_price}.

    Link to product: {entry.url}

    """
    text = f"Subject: {subject}\n{message}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_pass)
    server.sendmail(sender_email, target_email, text)
'''

if __name__ == "__main__" :
    
    PID = input("PID: ")
    p_name = product_name(PID) #returns name
    print(p_name)
    print(product_info(PID, '00'))

 



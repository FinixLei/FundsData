# coding=utf-8

import simplejson

def get_price_list(target_id): 
    content = ''
    with open("./all_data.txt", "r") as infile:
        content = infile.read()

    total_hash = simplejson.loads(content)
    
    price_list = []
    id_keys = sorted(total_hash[target_id].keys())
    for date in id_keys:
        if date != 'title':
            price_list.append((date, total_hash[target_id][date]))
    
    index = 0    
    for item in price_list:
        print index, item
        index += 1
        
    return price_list
    

def calculate(price_list, init_index, all_money):
    rest_money = all_money
    current_units = 0

    init_price = price_list[init_index][1]
    current_index = init_index + 1
    base_price = init_price
    
    plans = {
        'SELL_0.6': {'percent': -0.6}, 
        'SELL_0.8': {'percent': -0.8}, 
        'SELL_ALL': {'percent': -1}, 
        'BUY_0.6': {'percent': 0.6},
        'BUY_0.8': {'percent': 0.8},
        'BUY_ALL': {'percent': 1}
    }
    current_plan = None 
    
    while current_index < len(price_list):
        operation_flag = 0
        current_price = price_list[current_index][1]

        if current_plan is not None:
            op_percent = abs(plans[current_plan]['percent'])
            
            if plans[current_plan]['percent'] < 0:  # sell it
                if current_units > 0:
                    rest_money += current_price * current_units * op_percent
                    current_units *= (1 - op_percent)
                    operation_flag = 1
                else:  # Nothing to sell
                    pass
                    
            else:  # buy it
                if rest_money > 0:
                    current_units += rest_money * op_percent / current_price
                    rest_money *= (1 - op_percent)
                    operation_flag = 1
                else:  # No money to buy
                    pass
                
            if operation_flag:
                print "After this operation (index = %s), rest money is %s, current units are %s, current price is %s" \
                        % (current_index, rest_money, current_units, current_price)
            else:  
                print "No operation on (index = %s, date = %s, price = %s), Do nothing" \
                    % (current_index, price_list[current_index][0], price_list[current_index][1])
                    
        else:  # None plan
            print "On (index = %s, date = %s, price = %s), Do nothing" \
                    % (current_index, price_list[current_index][0], price_list[current_index][1])
                    
        total_money = rest_money + current_units * current_price
        result = "Draw"
        if total_money > all_money:
            result = "Win"
        elif total_money < all_money:
            result = "Lose"
            
        print "current_price=%s, current_units=%s, rest_money=%s, so total_money=%s, it's %s\n" \
                % (current_price, current_units, rest_money, total_money, result)

                
        delta = (current_price - base_price) / base_price

        if delta < -0.04: 
            current_plan = 'BUY_0.8'
        
        elif -0.04 <= delta < -0.02:
            current_plan = 'SELL_ALL'
        
        elif -0.02 <= delta < -0.01:
            current_plan = 'SELL_0.6'
            
        elif -0.01 <= delta < 0.15:
            # do nothing 
            pass
            
        elif 0.15 <= delta < 0.20:
            current_plan = 'SELL_0.8'
            
        elif 0.20 <= delta:
            current_plan = 'SELL_ALL'
            
        current_index += 1
        base_price = current_price if current_price > base_price else base_price
    
    
if __name__ == '__main__':
    # target_id = '000011'
    target_id = '233009'
    price_list = get_price_list(target_id)
    
    all_money = 10000.0
    init_index = 0
    calculate(price_list, init_index, all_money)
    
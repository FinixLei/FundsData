# coding=utf-8

import simplejson
import sys

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
    

def calculate(price_list, init_index, all_money, report_mode='short_line'):

    ### Step 1. Initialization
    
    init_price = price_list[init_index][1]
    rest_money = 0
    current_units = all_money / init_price
    
    current_index = init_index + 1
    base_price = init_price
    
    plans = {
        'SELL_MIDDLE': {'percent': -0.5}, 
        'SELL_LARGE':  {'percent': -0.8}, 
        'SELL_ALL':    {'percent': -1}, 
        'BUY_MIDDLE':  {'percent': 0.5},
        'BUY_LARGE':   {'percent': 0.8},
        'BUY_ALL':     {'percent': 1}
    }
    
    ### Step 2. Go Through the history data ###
    
    current_plan = 'No Plan'     
    while current_index < len(price_list):
        
        ### 2.1 Initialization ###
        
        operation_flag = 0
        date = price_list[current_index][0]
        current_price = price_list[current_index][1]

        ### 2.2 Execute the plan made on yesterday ###
        
        if current_plan != 'No Plan':
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

        else:  # No plan
            pass
        
        ### 2.3 Calculate the profit ### 
        
        op_msg = 'Did operation today' if operation_flag else 'No operation'
        total_money = rest_money + current_units * current_price
        result = "Draw"
        if total_money > all_money:
            result = "Win"
        elif total_money < all_money:
            result = "Lose"
            
        ### 2.4 Print Report ###
        
        if report_mode == 'long_line':
            if operation_flag != 0:
                DAILY_INFO = "%s - %s:\nplan=%s, real operation=%s, rest_money=%s, units=%s, current price=%s\ntotal money=%s, result=%s\n" \
                             % (current_index, date, current_plan, op_msg, rest_money, current_units, current_price, total_money, result)
            else:
                DAILY_INFO = "%(current_index)d - %(date)s: No Operation today" % {'current_index': current_index, 'date': date}
            print DAILY_INFO
            
        else: 
            INFO = []
            INFO.append("[%s] - %s:" % (current_index, date))
            INFO.append("operation:     %s" % op_msg)
            if operation_flag != 0:
                INFO.append("plan:          %s" % current_plan)
                INFO.append("rest money:    %s" % rest_money)
                INFO.append("units:         %s" % current_units)
                INFO.append("current_price: %s" % current_price)
                INFO.append("total money:   %s" % total_money)
                INFO.append("result: %s\n"    % result)
            for item in INFO:
                print item
        
        ### 2.5 Make Plan for Tomorrow ###
        
        delta = (current_price - base_price) / base_price

        if delta < -0.2: 
            current_plan = 'BUY_LARGE'
        
        elif -0.2 <= delta < -0.10:
            current_plan = 'SELL_ALL'
        
        elif -0.10 <= delta < -0.05:
            current_plan = 'SELL_MIDDLE'
            
        elif -0.05 <= delta < 0.05:
            # do nothing 
            pass
            
        elif 0.05 <= delta < 0.10:
            current_plan = 'SELL_MIDDLE'
            
        elif 0.10 <= delta:
            current_plan = 'SELL_ALL'
            
        current_index += 1
        # base_price = current_price if current_price > base_price else base_price
    
    
if __name__ == '__main__':
    target_id = '213008'
    # target_id = '233009'
    price_list = get_price_list(target_id)
    
    all_money = 10000.0
    init_index = 0
    report_mode = sys.argv[1] if len(sys.argv) >= 2 else 'short_line'    
    calculate(price_list, init_index, all_money, report_mode=report_mode)
    
'''Responsible for Writing Customized NetLogo models for EMD'''
class NetLogoWriter:
    __original_model_path = ""
    __rule_injected_model_path = ""
    EMD_line = -1000
    
    '''locate the NetLogo file, read it in, and identify the line to be experimented with as EMD_line.'''
    def __init__(self, model_string):
        __original_model_path = model_string
        #find EMD entry point
        with  open(__original_model_path, 'r') as file_reader:#should probably catch an exception here

            for i, line in enumerate(file_reader):
                if ";;insert evolutionary code here" in line:
                    print(i)
                    print(line)
                    EMD_line = i + 1
                
    '''if EMD annotation exists, then inject the new rule string'''
    def injectNewRule (self, new_rule):
        # with is like your try .. finally block in this case
        with open(__original_model_path, 'r') as file:  #should probably catch an exception here
            # read a list of lines into data
            data = file.readlines()
            file.close()
        __rule_injected_model_path
        if EMD_line >= 0:
            print( "Your line: " + data[EMD_line])
            data[EMD_line] = new_rule
            print(data)
            # and write everything back
            with open(__rule_injected_model_path, 'w') as file:
                file.writelines( data )
                file.flush()
                file.close()
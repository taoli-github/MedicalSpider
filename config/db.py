# db config
default_oracle_user = 'reason'
default_oracle_pwd = 'reason'
default_oracle_connect_str = '10.68.4.53:1521/hdw'

main_connect_str = '%s/%s@%s' % (default_oracle_user, default_oracle_pwd, default_oracle_connect_str)

mobile_user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) ' \
                    'Version/10.0 Mobile/14A456 Safari/602.1'
windows_phone_user_agent = 'Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                           'Chrome/58.0.3029.110 Mobile Safari/537.36 Edge/15.14900'
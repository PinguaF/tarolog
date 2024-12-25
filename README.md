
# -- In Develop -- In Develop -- In Develop --

# tarolog
**Python telegram bot. TeleBot Api. Try it!**  
Main file - main.py  
Configure your progect - config/config.py - Tokens  
                    or - config/lang-ru-0.json - Language  

# Versions
main branch:  
ver0.1 - released with goroskop  
develop brahcn:    
n1 - main ver0.1 clone  
n2 - added class User for DB  

# Class in project
Class `User` in project:  
locate in db.db  
    Atribut:  
    `User.Id` - [int] - telegram id of user  
    `User.Username` - [str] - telegram username  
    `User.CountCard` - [int] - count of cards(coins)  
    `User.Subscription` - [bool] - check subscrition to everyday message  
    `User.TypeAstrolog` - [int] - type of astrolog (0-2)  
    `User.Zodiak` - [int] - type of Zodiak (0-11)  
    `User.Role` - [str] - type of role(now admin, user)  
    `User.Claimed` - [bool] - is today award cleimed?  
    Methods:  


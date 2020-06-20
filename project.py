from collections import *
import re
import pickle as pk    
import sys



class Customer(Exception):
    try:
        totals=[]
        file=open('items.txt','r')
        item=file.readline().split()
        t=file.tell()
        file.seek(t)
        p=file.readline().split()
        file.close()

        I={}
        for i in range(0,len(item),2):
            I[item[i]]=int(item[i+1])
        price={}
        for i in range(0,len(p),2):
            price[p[i]]=int(p[i+1])

            
    except KeyboardInterrupt:
        print('SOMETHING WENT WRONG'.center(115,'_'))
        sys.exit()

    def Input(self):
        try:
            
            print('FILL FORM'.center(115,'_'))
            self.name=input('{:40}'.format('Enter Name'))
            self.add=input('{:40}'.format('Enter Address'))
            self.total=0
            self.bought={}
            self.cart=[]
            self.mobile_no=input('{:40}'.format('Enter mobile no'))
            print('_'*115)
        except KeyboardInterrupt:
            print('_'*115,end='\n\n')
            return
        except Exception:
            print('_'*115,end='\n\n')
            return
        
    def order(self):
        print('\n\n')
        print('ORDER'.center(115,'_'))
        choices={}
        for i,j in enumerate(Customer.I,start=1):
            choices[i]=j

        for i in choices:
            print(i,'. ',choices[i])
            
        print('Enter Done for place order')
        while True:
            try:
                n=int(input('{:10}: '.format('enter choice')))
                if Customer.I[choices[n]]<=self.cart.count(choices[n]):
                    print('We dont have more {}'.format(choices[n]))
                else:
                    self.cart.append(choices[n])
            except ValueError:
                self.bought=Counter(self.cart)
                print('_'*115,end='\n\n')
                return
            except KeyboardInterrupt:
                print('_'*115,end='\n\n')
                break

            except Exception:
                print('something went wrong')
                print('_'*115,end='\n\n')
                return
                
                
        
        
        
    def check_out(self):
        print('AVAILABLE ITEMS'.center(115,'_'))
        print('{:<20}{:<20}{:<20}'.format('Items','Quantity','PRICE($)'))
        try:
            for key in Customer.I:
                print('{:<20}{:<20}{:<20}'.format(key,Customer.I[key],Customer.price[key]))
            print('_'*115,end='\n\n')
        except KeyboardInterrupt:
            print('_'*115,end='\n\n')
            return


            
    def bill(self):
        print('BILL'.center(115,'_'))
        print('{:40}{}\n{:40}{}\n{:40}{}\n'.format('NAME',self.name,'CONTACT NUMBER',self.mobile_no,'ADDRESS',self.add))
        pr=0
        print('Itme'.ljust(30,' ')+'Quantity'.ljust(30,' ')+'PRICE($)'.ljust(30,' '))
        for p in self.bought:
            print('{:<30}{:<30}{:<30}'.format(p,self.bought[p],self.bought[p]*Customer.price[p]))
            pr+=self.bought[p]*Customer.price[p]
        self.total=pr
        s='Total: '+str(self.total)+'$/-'
        print(s.rjust(90,'_'),end='\n\n')
        
        Customer.I=Counter(Customer.I)
        Customer.I.subtract(self.bought)
        file=open('items.txt','w')
        for i in Customer.I:
            file.write(i+' '+str(Customer.I[i])+' ')
        file.write('\n')
        for i in Customer.price:
            file.write(i+' '+str(Customer.price[i])+' ')
        file.close()
        print('THANK YOU'.center(115,'_'),end='\n\n')
        file=open('customer.bin','ab')
        pk.dump(self,file)
        file.close()

        
    # Admin function   
    def customerlist(self):
        print('{:<30}{:<15}{:<50}{:<10}'.format(self.name,self.mobile_no,self.add,self.total))



class Admin:
    username='harsh vijay'
    password='harsh123'
    def __init__(self):
        try:
            for i in range(3):
                self.username=input('{:40}'.format('Enter Username'))
                self.password=input('{:40}'.format('Enter Password'))
                if self.username==Admin.username and self.password==Admin.password:
                    break
                elif i==2:
                    return
                else:
                    print('Invalid username or password'.center(115,'_'))
        except KeyboardInterrupt:
            print('_'*115)
            return
        except Exception:
            print('_'*115)
            return

        choice={1: Admin.ImoportStock,2:Admin.check_customer_detail}
        while True:
            try:
                print('MENU'.center(115,'_'))
                print('1. IMPORT STOCK\n2. CHECK CUSTOMER DETAIL\n3. EXIT\n')
                ch=int(input('CHOICE: '))
                print('_'*115)
                if ch==3:
                    break
                else:
                    choice[int(ch)](self)
            except KeyboardInterrupt:
                print('_'*115)
                return
            except Exception as e:
                print(e)
              
        

    def ImoportStock(self):
        Customer.check_out(self)
        print('ENTER ITMES LIST SEPERATED BY \',\' :')
        try:
            while True:
                l=list(map(str,input().split(',')))
                break
        except Exception:
            print('INVALID INPUT'.center(115,'_'))
            print('WRITE IT AGAIN'.center(115,' '))


        d={}
        p={}
        try:
            while True:
                print('{:<30} {:<30}'.format('ITEM','QUANTITY'))
                for item in l:
                    d[item]=int(input('{:<30} '.format(item)))

            
                print('{:<30} {:<30}'.format('ITEM','PRICE'))
                for item in l:
                    p[item]=int(input('{:<30} '.format(item)))
                break
        except Exception:
            print('SOMETHING WENT WRONG'.center(115,' '))
        d=Counter(d)
        l=list(d.elements())
        Customer.I=Counter(Customer.I)
        lst=list(Customer.I.elements())
        lst=l+lst
        Customer.I=Counter(lst)

        
        Customer.price.update(p)
        
        print('DONE'.center(115,'_'))
        Customer.check_out(self)
        file=open('items.txt','w')
        for i in Customer.I:
            file.write(i+' '+str(Customer.I[i])+' ')
        file.write('\n')
        for i in Customer.price:
            file.write(i+' '+str(Customer.price[i])+' ')
        file.close()
        
        
            
        
        


    def check_customer_detail(self):
        print('{:<30}{:<15}{:<50}{:<10}'.format('C-Name','C-Contact','Address','Bill'))
        file=open('customer.bin','rb')
        while True:
            try:
                l=pk.load(file)
                print('{:<30}{:<15}{:<50}{:<10}'.format(l.name,l.mobile_no,l.add,l.total))
                continue
            except FileNotFoundError:
                print('NO FILE FOUND'.center(115,'* '))
            except EOFError:
                file.close()
                break
            except Exception as e:
                file.close()
                break
            else:
                file.close()
                break
                
if __name__=='__main__':
    choice={1: Customer.check_out,2:Customer.order,3:Customer.bill}
    stop=False
    while not stop:
        try:
            print('WANNA BUY SOMETHING..??'.center(115,'_'))
            print('PRESS ENTER..!'.center(115,' '))
            i=input()
            if i=='no':
                break
            if i=='admin':
                a=Admin()
                print('\n')
                continue
            
            c=Customer()
            c.Input()
            while True:
                print('MENU'.center(115,'_'))
                print('1. CHECK OUT\n2. ORDER\n3. BILL\n4. NOT INTRUSTED\n5. CLOSE')
                ch=input('\nENTER YOUR CHOICE :')
                print('_'*115)
                
                    
                if int(ch)==5:
                    stop=True
                    print('\n')
                    break
                
                elif int(ch)==4:
                    print('THANK YOU'.center(115,'_'))
                    print('HAVE A NICE DAY..!'.center(115,' '))
                    print('\n')
                    break

                else:
                    choice[int(ch)](c)
        except KeyboardInterrupt:
            print('_'*115)
            stop=True
            print('\n')
            break
        except Exception:
            print('SOMETHING WENT WRONG'.center(115,'_'),end='\n\n\n')
            break
            

                
    

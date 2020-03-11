#123
##Roadmap## Basic -- Magic - in progress
#Ranged weapons
#Enemy inventory/item drops
#New Enemies
    #encounters based on character level.
#Enemy levels, adjusting enemy stats based on levels, dynamic to character level.
#More weapons/armor/items
#Code clean up DON'T FUCKING IGNORE THIS LIKE I KNOW YOU'RE GOING TO
#Enchantments > enchantedWeapon class?
#Enhanced magic
#Saving/loading
#Map/movement
#npcs/merchants
#story
#visuals? probably get started on other languages at this point, dude
#

def main():
    from random import randint
    from math import ceil

    #simulate die rolls
    def dieRoll(sides):
        roll = randint(1,sides)
        return roll

    class item():
        def __init__(self, name, val, wt, eff, cls):
            self.name = name
            self.val = val
            self.wt = wt
            self.eff = eff
            #for weapons = atk stat, armor = dfn stat, potion = heal amt
            self.cls = cls
            #cls = Melee, Ranged, armor, hRestore, mRestore, misc, money, stRestore

    #items#
    ironDagger = item('Iron Dagger',5,2,5,'melee')
    ironSword = item('Iron Sword',10,10,10,'melee')
    masterSword = item('Master Sword',1000,1,9999,'melee')
    
    woodenBow = item('Wooden Bow',3,2,5,'ranged')
    
    raggedyShirt = item('Raggedy Shirt',1,1,1,'armor')
    ironArmor = item('Iron Armor',13,15,10,'armor')
    
    hPotion = item('Health Potion',5,0,10,'hRestore')
    mPotion = item('Mana Potion',5,0,10,'mRestore')
    
    ironArrow = item('Iron Arrow',1,1,2,'misc')
    
    gold = item('Gold',1,0,0,'money')
    
    nullItem = item('None',0,0,0,'')
    fists = item('Fists',0,0,1,'melee')

    itemRef = {ironDagger.name:ironDagger,
               ironSword.name:ironSword,
               masterSword.name:masterSword,
               woodenBow.name:woodenBow,
               raggedyShirt.name:raggedyShirt,
               ironArmor.name:ironArmor,
               hPotion.name:hPotion,
               mPotion.name:mPotion,
               ironArrow.name:ironArrow,
               gold.name:gold,
               nullItem.name:nullItem,
               fists.name:fists}

    
    class spells():
        def __init__(self,name, val, eff, cost, cls):
            self.name = name
            self.val = val  #merch value
            self.eff = eff  #effect value, varies by class
            self.cost = cost  #MP cost
            self.cls = cls  #class:atk, restore, stRestore, status

    #spells# *cls is a list as spells may have multiple classes/effects. Single class spells are still a list for consistency's sake
    fireBall = spells('Fireball',25,5,3,['atk'])
    shock = spells('Shock',25,5,3,['atk'])
    tomFoolery = spells('Tomfoolery',250,25,10,['atk'])
    heal = spells('Heal',20,5,2,['restore'])


    def classSelect():
        charClasses = {'human': 5,
                       'gazorpazorp': 5,
                       'monkey': 10,
                       'hobbit': 4
                       }
        confirm = 'n'
        while confirm == 'n':
            print('In a land of chimpanzees, you are a: ')
            for item in charClasses:
                print('- {}'.format(item))
            charSelect = input()
            if charSelect in charClasses:
                print('Okay, you\'re a',charSelect,'then. Great.')
                confirm = 'y'
            else:
                print('So you\'re a',charSelect +'. Are you sure? Y/N')
                sure = input()
                if sure.lower() == 'y':
                    charClasses.setdefault(charSelect, 0)
                    confirm = sure
                else:
                    continue
        return charClasses[charSelect]

    class character():
        def __init__(self, name, hp, maxHp, mp, maxMp, atk, dfn, cls, inv, hit, xp):
            self.name = name
            self.hp = hp
            self.maxHp = maxHp
            self.mp = mp
            self.maxMp = maxMp
            self.atk = atk
            self.dfn = dfn
            self.cls = cls
            self.inv = inv
            self.hit = hit
            self.xp = xp


    class player(character):
        def __init__(self):
            super().__init__(input('What is your name?'),50,50,5,5,5,5,'',{'Consumables':{hPotion:3},'Gear':{ironSword:1,ironArmor:1},'Trinkets':{}},10,0)
        lvl = 1
        lvlUp = 10
        ranged = 6
        eqMelee = ironDagger
        eqRanged = nullItem
        eqArmor = raggedyShirt
        spells = [fireBall, tomFoolery]

        skillPoints = classSelect()
        
    hero = player()

    #Menus
    #main
    def fight():
        nonlocal hero,opponent,newEnc
        pRoll = dieRoll(20)
        mRoll = dieRoll(20)
        crit = 'n'
        fail = 'n'
        pDmg = 0
        mDmg = 0
        if pRoll == 20:     #d20 is rolled. if player.hit is <= roll, then hit. if 20 -> crit=Y 2x dmg, if 0 -> fail=Y 1//2 damage to self.
            crit = 'y'
        if pRoll == 0:
            fail = 'y'
        
        if pRoll < hero.hit:
            print(hero.name,'misses!')
        else:
            pDmg = randint(1,round((hero.atk*hero.eqMelee.eff)/opponent.dfn))     #calculate dmg range, and return random value = pDmg
            if fail == 'y':
                pDmg //= 2
                hero.hp -= pDmg
                print('Critical fail!',hero.name,'dealt',pDmg,'to themselves!')           
            else:
                if crit == 'y':
                    pDmg += round(((hero.atk*hero.eqMelee.eff)/opponent.dfn))
                    opponent.hp -= pDmg
                    print('Critical hit!',hero.name,'dealt',pDmg,'damage!')
                else:
                    opponent.hp -= pDmg
                    print(hero.name,'dealt',pDmg,'damage!')
        if opponent.hp < 1:
            print(opponent.name,'is defeated!')       #then we check if the monster has been defeated, or if we continue to the monster's attack
            newEnc = 1
            opponent.hp = opponent.maxHp    #revive the base monster, so you don't encounter an already dead one
            victory()       #xp gain, lvl up
            encounter()     #new encounter
        else:
            if mRoll < opponent.hit:
                print(opponent.name,'missed!')
            else:
                mDmg = randint(1,round((opponent.atk*10)/(hero.dfn+hero.eqArmor.eff))+1)
                hero.hp -= mDmg
                print(opponent.name,'dealt',mDmg,'damage!')
        if hero.hp < 1:
            print('You dead, son.\n')
            main()
        encounter()
    def magic():
        pass
    def inventory():
        print('\n    ---Inventory---')
        print('  Consumables:')
        for k,v in hero.inv['Consumables'].items():
            print('    '+k.name,'- Effect Pts:'+str(k.eff),'- qty:',v)
        print('  Gear:')
        for k,v in hero.inv['Gear'].items():
            print('    '+k.name,'- Atk/Def:'+str(k.eff),'- qty:',v)
        print('  Trinkets:')
        for k,v in hero.inv['Trinkets'].items():
            print('    '+k.name,'- Value:'+str(k.val),'- qty:',v)
        print()
        encMenu.invMenu()

    def changeEquip():
        print('\n-Equip or Unequip?\n "b" to go back.')
        choice = input()
        ##equip##
        if choice.lower() == 'equip' or choice.lower() == 'e':
            while True:
                print('''
    ---Equipped Items---
  Melee:  {} - Atk:{}
  Ranged: {} - Atk:{}
  Armor:  {} - Def:{}
    '''.format(hero.eqMelee.name,hero.eqMelee.eff,hero.eqRanged.name,hero.eqRanged.eff,hero.eqArmor.name,hero.eqArmor.eff)+
    '\n-Type item name to equip.\n "b" to go back.\n    ---Equippable Items---')
                for i in hero.inv['Gear'].keys():
                    print('  ',i.name,'Atk/Def:'+str(i.eff))
                itemName = input().title()
                print()
                if itemName.lower() == 'b':
                    break
                elif itemName not in itemRef.keys():
                    print('Invalid selection.\n-Type item name to equip.\n "b" to go back.')
                    continue
                key = itemRef[itemName]
                if key in hero.inv['Gear'].keys():  #check for requested item in inventory
                    if key.cls == 'melee':
                        if hero.eqMelee != fists:       #if no item is equipped yet, move on, otherwise add equipped item to inventory
                            hero.inv['Gear'].setdefault(hero.eqMelee, 0)
                            hero.inv['Gear'][hero.eqMelee] += 1
                            print(hero.eqMelee.name,'unequipped')
                        hero.eqMelee = key
                    if key.cls == 'ranged':
                        if hero.eqRanged != nullItem:
                            hero.inv['Gear'].setdefault(hero.eqRanged, 0)
                            hero.inv['Gear'][hero.eqRanged] += 1
                            print(hero.eqRanged.name,'unequipped')
                        hero.eqRanged = key
                    if key.cls == 'armor':
                        if hero.eqArmor != nullItem:
                            hero.inv['Gear'].setdefault(hero.eqArmor, 0)
                            hero.inv['Gear'][hero.eqArmor] += 1
                            print(hero.eqArmor.name,'unequipped')
                        hero.eqArmor = key
                    print(key.name,'equipped')
                    hero.inv['Gear'][key] -= 1
                    if hero.inv['Gear'][key] == 0:
                        del hero.inv['Gear'][key]
                    continue
                else:
                    print('Cannot equip this item. Select something else.\n-Type item name to equip.\n "b" to go back.')
            inventory()
        ##Unequip##     
        elif choice.lower() == 'unequip' or choice.lower() == 'u':
            while True:
                print('''
   -Type item name to unequip.
   "b" to go back.
    ---Equipped Items---
  Melee:  {} - Atk:{}
  Ranged: {} - Atk:{}
  Armor:  {} - Def:{}'''.format(hero.eqMelee.name,hero.eqMelee.eff,hero.eqRanged.name,hero.eqRanged.eff,hero.eqArmor.name,hero.eqArmor.eff))
                choice = input().title()
                print()
                if choice == 'None' or choice == 'Fists':
                    print('\nFunny guy, eh?')
                    continue
                elif choice == hero.eqMelee.name or choice == 'Melee':
                    if hero.eqMelee == fists:
                        print('\nNo-can-doos-ville. Try again.')
                        continue
                    hero.inv['Gear'].setdefault(hero.eqMelee,0)
                    hero.inv['Gear'][hero.eqMelee] += 1
                    print(hero.eqMelee.name,'unequipped')
                    hero.eqMelee = fists
                    continue
                elif choice == hero.eqRanged.name or choice == 'Ranged':
                    if hero.eqRanged == nullItem:
                        print('\nNo-can-doos-ville. Try again.')
                        continue
                    hero.inv['Gear'].setdefault(hero.eqRanged,0)
                    hero.inv['Gear'][hero.eqRanged] += 1
                    print(hero.eqRanged.name,'unequipped')
                    hero.eqRanged = nullItem
                    continue
                elif choice == hero.eqArmor.name or choice == 'Armor':
                    if hero.eqArmor == nullItem:
                        print('\nNo-can-doos-ville. Try again.')
                        continue
                    hero.inv['Gear'].setdefault(hero.eqArmor,0)
                    hero.inv['Gear'][hero.eqArmor] += 1
                    print(hero.eqArmor.name,'unequipped')
                    hero.eqArmor = nullItem
                    continue
                elif choice.lower() == 'b':
                    break
                else:
                    print('\nInvalid selection.')
            inventory()
        else:
            inventory()

    def useItem():
        while True:
            print('\n-Type item name to use.\n "b" to go back.\n    ---Usable Items---')
            for i in hero.inv['Consumables'].keys():
                print('   ',i.name,'Qty:',hero.inv['Consumables'][i])
            choice = input().title()
            key = itemRef[choice]
            if choice.lower() == 'b':
                break
            elif key not in hero.inv['Consumables'].keys():
                print('invalid selection')
                continue
            else:
                if key.cls == 'hRestore':
                    hero.hp += key.eff
                    hero.inv['Consumables'][i] -= 1
                    if hero.inv['Consumables'][i] == 0:
                        del hero.inv['Consumables'][i]
                    if hero.hp > hero.maxHp:
                        hero.hp = hero.maxHp
                        print('\n'+hero.name,'fully recovered!')
                        break
                    else:
                        print('\n'+hero.name,'recovered',key.eff,'hit points!')
                        break
                if key.cls == 'mRestore':
                    hero.mp += key.eff
                    hero.inv['Consumables'][i] -= 1
                    if hero.inv['Consumables'][i] == 0:
                        del hero.inv['Consumables'][i]
                    if hero.mp > hero.maxMp:
                        hero.mp = hero.maxMp
                        print('\n'+hero.name+'\'s mana is fully recovered!')
                        break
                    else:
                        print('\n'+hero.name,'recovered',key.eff,'mana!')
                        break                
        inventory()

            
    def info():
        print('''
    name: {}
    HP: {}/{}
    MP: {}/{}
    lvl: {}
    XP: {}/{}
    Melee Atk: {}
    Ranged Atk: {}
    Def: {}
    Acc: {}
    Melee Weap: {}
    Ranged Weap: {}
    Armor: {}
    '''.format(hero.name,hero.hp,hero.maxHp,hero.mp,hero.maxMp,hero.lvl,hero.xp,hero.lvlUp,hero.atk,hero.ranged,hero.dfn,hero.hit,hero.eqMelee.name,hero.eqRanged.name,hero.eqArmor.name))
        print()
        encMenu.encMain()
    def checkMap():
        pass

    def rewind():
        encMenu.encMain()

    class encMenu:
        main = {'f': ('Fight',fight),
                'm': ('Magic: '+str(hero.mp)+'mp',magic),
                'i': ('Inventory',inventory),
                'p': ('Info',info)}
        inv = {'c': ('Change Equipment',changeEquip),
               'u': ('Use Item', useItem),
               'b': ('Back', rewind)}
        def encMain():
            for k,v in encMenu.main.items():
                print(k+': ',v[0])
            choice = ''
            while True:
                choice = input()
                if choice in encMenu.main.keys():
                    break
                else:
                    continue
            encMenu.main[choice][1]()
            
        def invMenu():
            for k,v in encMenu.inv.items():
                print(k+': ',v[0])
            choice = ''
            while True:
                choice = input()
                if choice in encMenu.inv.keys():
                    break
                else:
                    continue
            encMenu.inv[choice][1]()

    def skillSet(points):
        pts = points
        while pts > 0:
            options = ['hp','mp','atk','ranged','dfn','hit']
            print('You have',pts,'points to assign. Where would you like to put them?')
            print('hp:',hero.hp,'\n'
                  'mp:',hero.mp,'\n'
                  'atk:',hero.atk,'\n'
                  'ranged:',hero.ranged,'\n'
                  'dfn:',hero.dfn,'\n'
                  'hit:',hero.hit)
            while True:
                choice = input()
                if choice.lower() == 'hp':
                    hero.hp += 1
                    break
                elif choice.lower() == 'mp':
                    hero.mp += 1
                    break
                elif choice.lower() == 'atk':
                    hero.atk += 1
                    break
                elif choice.lower() == 'ranged':
                    hero.ranged += 1
                    break
                elif choice.lower() == 'dfn':
                    hero.dfn += 1
                    break
                elif choice.lower() == 'hit':
                    hero.hit -= 1
                    break
                else:
                    print('Please select a valid skill')
                    continue
            pts -= 1
        print('\nStats set!\n'
              'hp:',hero.hp,'\n'
              'mp:',hero.mp,'\n'
              'atk:',hero.atk,'\n'
              'ranged:',hero.ranged,'\n'
              'dfn:',hero.dfn,'\n'
              'hit:',hero.hit)


    skillSet(hero.skillPoints)

    #(name, hp, maxHp, mp, maxMp, atk, dfn, cls, inv, hit, xp) character stats order for reference
    enemyBoar = character('Wild Boar',35,35, 0,0, 2, 3, '', {}, 14, 3)
    enemyImp = character('Feral Imp',40,40, 0,0, 3, 2, '', {}, 13, 4)
    enemyOrc = character('Orc',50,50, 0,0, 4, 4, '', {}, 11, 6)

    enemies = [enemyBoar,enemyImp,enemyOrc]
    #make disctionary with level values as keys, lists of monsters as values for ecnountering
    #certain monsters at certain levels

    opponent = 0
    newEnc = 1
    def encounter():
        nonlocal newEnc,opponent
        if newEnc == 1:
            opponent = enemies[randint(0,len(enemies)-1)]
            newEnc = 0
            print('''
    A {} appeared!
    What will you do?.....{}: {}/{}hp
                     .....{}: {}/{}hp'''.format(opponent.name,opponent.name,opponent.hp,opponent.maxHp,hero.name,hero.hp,hero.maxHp))
            encMenu.encMain()
        else:
            print('''
    What will you do?.....{}: {}/{}hp
                     .....{}: {}/{}hp'''.format(opponent.name,opponent.hp,opponent.maxHp,hero.name,hero.hp,hero.maxHp))
            encMenu.encMain()

    def victory():
        hero.xp += opponent.xp
        print('You gained',str(opponent.xp)+'xp!')
        if hero.xp >= hero.lvlUp:
            hero.lvl += 1
            hero.lvlUp = ceil(hero.lvlUp*1.5)
            hero.maxHp += ceil(hero.maxHp*0.1)
            hero.hp += ceil(hero.maxHp*0.1)
            hero.maxMp += ceil(hero.maxMp*0.1)
            hero.mp += ceil(hero.maxMp*0.1)
            hero.atk += ceil(hero.atk*0.1)
            hero.ranged += ceil(hero.ranged*0.1)
            hero.dfn += ceil(hero.dfn*0.1)
            if hero.hit > 0 and (hero.lvl % 3) == 0:
                    hero.hit -= 1
            print('''
    {} reached level {}!
    HP: {}
    MP: {}
    Atk: {}
    Ranged: {}
    Def: {}
    Hit: {}'''.format(hero.name, hero.lvl, hero.maxHp, hero.maxMp, hero.atk, hero.ranged, hero.dfn, hero.hit))

    encounter()

if __name__ == '__main__':
        main()
        
###


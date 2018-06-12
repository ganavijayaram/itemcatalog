from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setupwithusers import Category, Base, User,Item

engine = create_engine('sqlite:///itemcatelogwithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

#users
User1 = User(name="Ganavi", email="ganavijayaram1996@gmailcom",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()


User2 = User(name="Vinay Kowdle", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User2)
session.commit()

#items for Engineering Streams
category1 = Category(user_id=1,name="Engineering Streams")
session.add(category1)
session.commit()

item1 = Item(user_id=1,name="Computer Science Engineering",description="Computer science and engineering (CSE)"+
             "is an academic program at some universities that integrates the fields of computer engineering"+
             "and computer science. ... The program also includes core areas of computer science such as"+
             "theory of computation, operating systems, design and analysis of algorithms and data structures.",category=category1)
session.add(item1)
session.commit()

item2 = Item(user_id=1,name="Electronics and Communication Engineering",description="Electronic engineering (also called electronics "+
             "and communications engineering) is an electrical engineering discipline which utilizes "+
             "nonlinear and active electrical components (such as semiconductor devices, especially"+
             "transistors, diodes and integrated circuits) to design electronic circuits, devices, VLSI devices"+
            "and their systems. The discipline typically also designs passive electrical components, usually"+
             "based on printed circuit boards.",category=category1)
session.add(item2)
session.commit()

item3 = Item(user_id=1,name="Civil Engineering",description="Civil engineering is a professional engineering discipline that"+
             "deals with the design, construction, and maintenance of the physical and naturally built environment,"+
             "including works such as roads, bridges, canals, dams, airports, sewerage systems, pipelines, and railways."+
             "Civil engineering is traditionally broken into a number of sub-disciplines. It is the second-oldest engineering"+
             "discipline after military engineering,[3] and it is defined to distinguish non-military engineering from military"+
             "engineering.[4] Civil engineering takes place in the public sector from municipal through to national governments,"+
             "and in the private sector from individual homeowners through to international companies.",category=category1)
session.add(item3)
session.commit()
             
item4 = Item(user_id=1,name="Mechanical Engineering",description="The mechanical engineering field requires an understanding"+
             "of core areas including mechanics, dynamics, thermodynamics, materials science, structural analysis,"+
             "and electricity. In addition to these core principles, mechanical engineers use tools such as "+
             "computer-aided design (CAD), computer-aided manufacturing (CAM), and product life cycle management"+
             "to design and analyze manufacturing plants, industrial equipment and machinery, heating and cooling "+
             "systems, transport systems, aircraft, watercraft, robotics, medical devices, weapons, and others. It "+
             "is the branch of engineering that involves the design, production, and operation of machinery",category=category1)
session.add(item4)
session.commit()
             
#items for Code Editors
category2 = Category(user_id=1,name="Code Editors")
session.add(category2)
session.commit()

item1 = Item(user_id=1,name="Atom",description="Atom is a free and open-source text and source code"+
             "editor for macOS, Linux, and Microsoft Windows[6] with support for plug-ins "+
             "written in Node.js, and embedded Git Control, developed by GitHub. Atom is a desktop"+
             "application built using web technologies.[7] Most of the extending packages have free"+
             "software licenses and are community-built and maintained.[8] Atom is based on Electron"+
             "a framework that enables cross-platform desktop applications using Chromium and Node.js."+
             "It is written in CoffeeScript and Less.[12] It can also be used as an integrated development "+
             "environment (IDE).",category=category2)
session.add(item1)
session.commit()

item2 = Item(user_id=1,name="Sublime",description="Sublime Text is a proprietary cross-platform source code editor"+
             "with a Python application programming interface (API). It natively supports many programming "+
             "languages and markup languages, and functions can be added by users with plugins, typically "+
             "community-built and maintained under free-software licenses.",category=category2)
session.add(item2)
session.commit()

item3 = Item(user_id=1,name="Eclipse",description="Eclipse software development kit (SDK) is free and open-source software, "+
             "released under the terms of the Eclipse Public License, although it is incompatible with the GNU General"+
             "Public License.[10] It was one of the first IDEs to run under GNU Classpath and it runs without"+
             "problems under IcedTea.",category=category2)
session.add(item3)
session.commit()

item4 = Item(user_id=1,name="Coda",description="Coda is a commercial and proprietary web development application "+
             "for macOS, developed by Panic. It was released on April 23, 2007 and won the 2007 Apple "+
             "Design Award for Best User Experience. Coda version 2.0 was released on 24 May 2012, "+
             "along with an iPad version called Diet Coda. Although formerly available on the Mac App"+
             "Store, it was announced on May 14, 2014 that the update to Coda 2.5 would not be available "+
             "in the Mac App Store due to sandboxing restrictions.[2]",category=category2)
session.add(item4)
session.commit()

#items for Front-end Frameworks
category3 = Category(user_id=1,name="Front-end Frameworks")
session.add(category3)
session.commit()

item1 = Item(user_id=1,name="Angular",description="Angular 2+ or Angular v2 and above"+
             "is a TypeScript-based open-source front-end web application platform "+
             "led by the Angular Team at Google and by a community of individuals "+
             "and corporations. Angular is a complete rewrite from the same team that "+
             "built AngularJS.",category=category3)
session.add(item1)
session.commit()

item2 = Item(user_id=1,name="React",description="React can be used in the development"+
             " of single-page applications and mobile applications. It aims"+
             "primarily to provide speed, simplicity, and scalability. As a"+
             "user interface library, React is often used in conjunction with"+
             "other libraries such as Redux.",category=category3)
session.add(item2)
session.commit()

#items for Back-end Frameworks
category4 = Category(user_id=1,name="Back-end Frameworks")
session.add(category4)
session.commit()

item1 = Item(user_id=1,name="Flask",description="Flask is a micro web framework"+
             "written in Python. It is classified as a microframework "+
             "because it does not require particular tools or libraries."+
             "It has no database abstraction layer, form validation, or any other components"+
             "where pre-existing third-party libraries provide common functions. However, Flask "+
             "supports extensions that can add application features as if they were implemented in"+
             "Flask itself. Extensions exist for object-relational mappers, form validation, upload "+
             "handling, various open authentication technologies and several common framework"+
             "related tools. ",category=category4)
session.add(item1)
session.commit()

item2 = Item(user_id=1,name="Express",description="Express.js, or simply Express, is a web application"+
             "framework for Node.js, released as free and open-source software under the MIT"+
             "License. It is designed for building web applications and APIs.[3] It has been "+
             "called the de facto standard server framework for Node.js.",category=category4)
session.add(item2)
session.commit()

#items for Adventures
category5 = Category(user_id=1,name="Adventures")
session.add(category5)
session.commit()

item1 = Item(user_id=1,name="Mountain Biking",description="Mountain biking is the sport of riding"+
             "bicycles off-road, often over rough terrain, using specially designed "+
             "mountain bikes. Mountain bikes share similarities with other bikes but "+
             "incorporate features designed to enhance durability and performance in rough terrain."+
             "Mountain biking can generally be broken down into multiple categories: cross country"+
             ", trail riding, all mountain (also referred to as 'Enduro'), downhill, freeride and dirt"+
             "jumping. However, the majority of mountain biking falls into the categories of Trail and"+
             "Cross Country riding styles.",category=category5)
session.add(item1)
session.commit()

item2 = Item(user_id=1,name="Paragliding",description="Paragliding is the recreational and competitive adventure"+
             "sport of flying paragliders: lightweight, free-flying, foot-launched glider aircraft with "+
             "no rigid primary structure.[1] The pilot sits in a harness suspended below a fabric wing."+
             "Wing shape is maintained by the suspension lines, the pressure of air entering vents in "+
             "the front of the wing, and the aerodynamic forces of the air flowing over the outside.",category=category5)
session.add(item2)
session.commit()

item3 = Item(user_id=1,name="Scuba Diving",description="Scuba diving is a mode of underwater diving where the"+
             "diver uses a self-contained underwater breathing apparatus (scuba) which is completely"+
             "independent of surface supply, to breathe underwater.[1] Scuba divers carry"+
             "their own source of breathing gas, usually compressed air,[2] allowing them "+
             "greater independence and freedom of movement than surface-supplied divers, and "+
             "longer underwater endurance than breath-hold divers.",category=category5)
session.add(item3)
session.commit()

#items for Games
category6 = Category(user_id=2,name="Games")
session.add(category6)
session.commit()

item1 = Item(user_id=2,name="Rainbow Six Siege",description="The game puts heavy emphasis on environmental"+
             "destruction and cooperation between players. Players assume control of an attacker"+
             "or a defender in different gameplay modes such as hostage rescuing and"+
             "bomb defusing. The title has no campaign but features a series of short"+
             "missions that can be played solo. These missions have a loose narrative,"+
             "focusing on recruits going through training to prepare them for future"+
             "encounters with the White Masks, a terrorist group that threatens the"+
             "safety of the world.",category=category6)
session.add(item1)
session.commit()

item2 = Item(user_id=2,name="Dark Souls 3",description="Dark Souls III was critically and commercially"+
             "successful, with critics calling it a worthy and fitting conclusion to the "+
             "series. It was the fastest-selling game in Bandai Namco's history, shipping "+
             "over three million copies worldwide within the first two months after release."+
             "Dark Souls III: The Fire Fades, a complete version containing the base game "+
             "and both downloadable content expansions, was released in April 2017.",category=category6)
session.add(item2)
session.commit()


#items for Hollywood Singers
category7 = Category(user_id=2,name="Hollywood Singers")
session.add(category7)
session.commit()

item1 = Item(user_id=2,name="Taylor Swift",description="Taylor Alison Swift (born December 13, 1989) "+
             "is an American singer-songwriter. One of the leading contemporary recording"+
             "artists, she is known for narrative songs about her personal life, which "+
             "have received widespread media coverage.",category=category7)
session.add(item1)
session.commit()

item2 = Item(user_id=2,name="Zayn",description="Zayn is an English singer and songwriter. Born "+
             "and raised in Bradford, West Yorkshire, Malik auditioned as a solo "+
             "artist for the British music competition The X Factor in 2010. After "+
             "being eliminated as a solo performer, Malik was brought back into the "+
             "competition, along with four other contestants, to form the boy band that"+
             "would become known as One Direction. Malik split from the group in March"+
             "2015 and signed a solo recording contract with RCA Records.",category=category7)
session.add(item2)
session.commit()

item3 = Item(user_id=2,name="Rihanna",description=" is a Barbadian singer, songwriter, actress, and businesswoman."+
             "Born in Saint Michael, Barbados and raised in Bridgetown, during 2003, she recorded demo "+
             "tapes under the direction of record producer Evan Rogers and signed a recording "+
             "contract with Def Jam Recordings after auditioning for its then-president, hip"+
             "hop producer and rapper Jay-Z. In 2005, Rihanna rose to fame with the release "+
             "of her debut studio album Music of the Sun and its follow-up A Girl like Me (2006), "+
             "which charted on the top 10 of the US Billboard 200 and respectively produced the"+
             "successful singles 'Pon de Replay', 'SOS' and 'Unfaithful'.",category=category7)
session.add(item4)
session.commit()

#items for DC Movies
category8 = Category(user_id=2,name="DC Movies")
session.add(category8)
session.commit()

item1 = Item(user_id=2,name="Justice League",description="The Justice League is a group of fictional superheroes"+
             "who appear in American comic books published by DC Comics. They were conceived by writer"+
             "Gardner Fox and first appeared as a team in The Brave and the Bold #28 (March 1960)",category=category8)
session.add(item1)
session.commit()


item2 = Item(user_id=2,name="The Dark Knight",description="The follow-up to Batman Begins, The Dark Knight"+
             "reunites director Christopher Nolan and star Christian Bale, who reprises "+
             "the role of Batman/Bruce Wayne in his continuing war on crime. With the help"+
             "of Lt. Jim Gordon and District Attorney Harvey Dent, Batman sets out to destroy "+
             "organized crime in Gotham for good.",category=category8)
session.add(item2)
session.commit()

#items for Marvel Movies
category9 = Category(user_id=2,name="Marvel Movies")
session.add(category9)
session.commit()

item1 = Item(user_id=2,name="Iron Man",description="Tony Stark is an engineering superhero! Although Tony Stark"+
             "doesn't have any super powers, he is an incredibly good engineer. Iron Man is Tony"+
             "Stark's creation. It's a special suit that gives Stark superhuman strength, the"+
             "ability to fly and powerful weapons.",category=category9)
session.add(item1)
session.commit()

item2 = Item(user_id=2,name="Doctor Strange",description="The Orb of Agamotto is a fictional magical"+
             "item in the Marvel Comics universe. It is a powerful scrying crystal ball owned "+
             "and used by Doctor Strange. It can also be used to detect magic in use anywhere "+
             "in the world and provide Strange with a location and visual.",category=category9)
session.add(item2)
session.commit()

item3 = Item(user_id=2,name="Captain America",description="Captain America has no superhuman powers, but"+
             "through the Super-Soldier Serum and 'Vita-Ray' treatment, he is transformed and "+
             "his strength, endurance, agility, speed, reflexes, durability, and healing are at"+
             "the zenith of natural human potential.",category=category9)
session.add(item3)
session.commit()

#items for Pets
category10 = Category(user_id=2,name="Pets")
session.add(category10)
session.commit()

item1 = Item(user_id=2,name="Dogs",description="They were originally bred from wolves. They have been"+
             "bred by humans for a long time, and were the first animals ever to be domesticated. "+
             "Today, some dogs are used as pets, others are used to help humans do their work."+
             "They are a popular pet because they are usually playful, friendly, loyal and listen"+
             "to humans.",category=category10)
session.add(item1)
session.commit()

item2 = Item(user_id=2,name="Cats",description="The domestic cat (Felis silvestris catus or"+
             "Felis catus) is a small, typically furry, carnivorous mammal. They "+
             "are often called house cats when kept as indoor pets or simply cats when "+
             "there is no need to distinguish them from other felids and felines.",category=category10)
session.add(item2)
session.commit()


#items for Drugs
category11 = Category(user_id=2,name="Drugs")
session.add(category11)
session.commit()

item1 = Item(user_id=2,name="Heroin",description="Heroin, also known as diamorphine among other names,"+
             "is an opioid most commonly used as a recreational drug for its euphoric effects."+
             "Medically it is used in several countries to relieve pain or in opioid replacement "+
             "therapy. Heroin is typically injected, usually into a vein; however, it can also"+
             "be smoked, snorted or inhaled.[2][10][11] Onset of effects is usually rapid and lasts "+
             "for a few hours.",category=category11)
session.add(item1)
session.commit()

item2 = Item(user_id=2,name="Cocaine",description="ocaine, also known as coke, is a strong stimulant mostly "+
             "used as a recreational drug.[10] It is commonly snorted, inhaled as smoke, or as a solution"+
             "injected into a vein.[9] Mental effects may include loss of contact with reality, an intense"+
             "feeling of happiness, or agitation.[9] Physical symptoms may include a fast heart rate, sweating,"+
             "and large pupils.[9] High doses can result in very high blood pressure or body temperature."+
             "Effects begin within seconds to minutes of use and last between five and ninety minutes."+
             "Cocaine has a small number of accepted medical uses such as numbing and decreasing bleeding "+
             "during nasal surgery",category=category11)
session.add(item2)
session.commit()




#items for Magazines
category12 = Category(user_id=2,name="Magazines")
session.add(category12)
session.commit()

item1 = Item(user_id=2,name="Vogue",description="Vogue (magazine) Vogue is a fashion and lifestyle magazine "+
             "covering many topics including fashion, beauty, culture, living, and runway. Vogue began"+
             "as a weekly newspaper in 1892 in the United States, before becoming a monthly publication"+
             "years later.",category=category12)
session.add(item1)
session.commit()

item2 = Item(user_id=2,name="Cosmopolitan",description="Cosmopolitan is an international fashion magazine for "+
             "women, which was formerly titled The Cosmopolitan. The magazine was first"+
             "published and distributed in 1886 in the United States as a family magazine;"+
             "it was later transformed into a literary magazine and eventually became a women's"+
             "magazine (since 1965).",category=category12)
session.add(item2)
session.commit()

item3 = Item(user_id=2,name="Fortune",description="Fortune is an American multinational business magazine headquartered in New York"+
             "City, United States. It is published and owned by Time Inc., itself owned "+
             "by Meredith Corporation. The publication was founded by Henry Luce in 1929.",category=category12)
session.add(item3)
session.commit()

item4 = Item(user_id=2,name="People",description="People is an American weekly magazine of celebrity and human-interest"+
             "stories, published by Meredith Corporation. With a readership of 46.6 million adults, People has "+
             "the largest audience of any American magazine. ... People's website, People.com, focuses on c"+
             "elebrity news and human interest stories.",category=category12)
session.add(item4)
session.commit()


print("added items")





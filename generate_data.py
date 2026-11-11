"""
Data generator for RecomAI - Smart Recommendation System
Generates curated catalogs and realistic interaction rating matrices
for Movies, Music, and Shopping items.
"""

import os
import json
import pandas as pd
import numpy as np

os.makedirs("data", exist_ok=True)
os.makedirs("src", exist_ok=True)

# -------------------------------------------------------------
# 1. MOVIES DATASET
# -------------------------------------------------------------
movies_data = [
    {
        "item_id": "MOV01",
        "title": "Inception",
        "genre": "Sci-Fi",
        "year": 2010,
        "rating": 8.8,
        "director": "Christopher Nolan",
        "duration": "2h 28m",
        "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
        "poster_url": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=800&q=80",
        "cast": "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page"
    },
    {
        "item_id": "MOV02",
        "title": "Interstellar",
        "genre": "Sci-Fi",
        "year": 2014,
        "rating": 8.7,
        "director": "Christopher Nolan",
        "duration": "2h 49m",
        "description": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot is tasked to pilot a spacecraft along with a team of researchers to find a new planet for humans.",
        "poster_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80",
        "cast": "Matthew McConaughey, Anne Hathaway, Jessica Chastain"
    },
    {
        "item_id": "MOV03",
        "title": "The Matrix",
        "genre": "Sci-Fi",
        "year": 1999,
        "rating": 8.7,
        "director": "Lana & Lilly Wachowski",
        "duration": "2h 16m",
        "description": "When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth--the life he knows is the elaborate deception of an evil cyber-intelligence.",
        "poster_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=800&q=80",
        "cast": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss"
    },
    {
        "item_id": "MOV04",
        "title": "Dune: Part Two",
        "genre": "Sci-Fi",
        "year": 2024,
        "rating": 8.8,
        "director": "Denis Villeneuve",
        "duration": "2h 46m",
        "description": "Paul Atreides unites with Chani and the Fremen while seeking revenge against the conspirators who destroyed his family amidst a spice-rich desert world.",
        "poster_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=800&q=80",
        "cast": "Timothée Chalamet, Zendaya, Rebecca Ferguson"
    },
    {
        "item_id": "MOV05",
        "title": "Blade Runner 2049",
        "genre": "Sci-Fi",
        "year": 2017,
        "rating": 8.0,
        "director": "Denis Villeneuve",
        "duration": "2h 44m",
        "description": "Young Blade Runner K's discovery of a long-buried secret leads him to track down former Blade Runner Rick Deckard, who's been missing for thirty years.",
        "poster_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=800&q=80",
        "cast": "Ryan Gosling, Harrison Ford, Ana de Armas"
    },
    {
        "item_id": "MOV06",
        "title": "The Dark Knight",
        "genre": "Action",
        "year": 2008,
        "rating": 9.0,
        "director": "Christopher Nolan",
        "duration": "2h 32m",
        "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
        "poster_url": "https://images.unsplash.com/photo-1509281373149-e957c6296406?auto=format&fit=crop&w=800&q=80",
        "cast": "Christian Bale, Heath Ledger, Aaron Eckhart"
    },
    {
        "item_id": "MOV07",
        "title": "Mad Max: Fury Road",
        "genre": "Action",
        "year": 2015,
        "rating": 8.1,
        "director": "George Miller",
        "duration": "2h 0m",
        "description": "In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search for her homeland with the aid of a group of female prisoners, a psychotic worshiper and an ex-drifter named Max.",
        "poster_url": "https://images.unsplash.com/photo-1511875762315-c773eb98eec0?auto=format&fit=crop&w=800&q=80",
        "cast": "Tom Hardy, Charlize Theron, Nicholas Hoult"
    },
    {
        "item_id": "MOV08",
        "title": "John Wick: Chapter 4",
        "genre": "Action",
        "year": 2023,
        "rating": 7.7,
        "director": "Chad Stahelski",
        "duration": "2h 49m",
        "description": "John Wick uncovers a path to defeating The High Table. But before he can earn his freedom, Wick must face off against a new enemy with powerful alliances across the globe.",
        "poster_url": "https://images.unsplash.com/photo-1579783902614-a3fb3927b675?auto=format&fit=crop&w=800&q=80",
        "cast": "Keanu Reeves, Donnie Yen, Bill Skarsgård"
    },
    {
        "item_id": "MOV09",
        "title": "Top Gun: Maverick",
        "genre": "Action",
        "year": 2022,
        "rating": 8.3,
        "director": "Joseph Kosinski",
        "duration": "2h 10m",
        "description": "After thirty years, Maverick is still pushing the envelope as a top naval aviator, but must confront ghosts of his past when he leads TOP GUN's elite graduates on an impossible mission.",
        "poster_url": "https://images.unsplash.com/photo-1517976487507-5b3b4a45097c?auto=format&fit=crop&w=800&q=80",
        "cast": "Tom Cruise, Miles Teller, Jennifer Connelly"
    },
    {
        "item_id": "MOV10",
        "title": "Gladiator",
        "genre": "Action",
        "year": 2000,
        "rating": 8.5,
        "director": "Ridley Scott",
        "duration": "2h 35m",
        "description": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.",
        "poster_url": "https://images.unsplash.com/photo-1461360370896-922624d12aa1?auto=format&fit=crop&w=800&q=80",
        "cast": "Russell Crowe, Joaquin Phoenix, Connie Nielsen"
    },
    {
        "item_id": "MOV11",
        "title": "Superbad",
        "genre": "Comedy",
        "year": 2007,
        "rating": 7.6,
        "director": "Greg Mottola",
        "duration": "1h 53m",
        "description": "Two co-dependent high school seniors are forced to deal with separation anxiety after their plan to stage a booze-soaked party goes awry.",
        "poster_url": "https://images.unsplash.com/photo-1514306191717-452ec28c7814?auto=format&fit=crop&w=800&q=80",
        "cast": "Jonah Hill, Michael Cera, Christopher Mintz-Plasse"
    },
    {
        "item_id": "MOV12",
        "title": "The Grand Budapest Hotel",
        "genre": "Comedy",
        "year": 2014,
        "rating": 8.1,
        "director": "Wes Anderson",
        "duration": "1h 39m",
        "description": "A writer encounters the owner of an aging high-class hotel, who tells him of his early years serving as a lobby boy in the hotel's glorious heyday under an exceptional concierge.",
        "poster_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80",
        "cast": "Ralph Fiennes, F. Murray Abraham, Mathieu Amalric"
    },
    {
        "item_id": "MOV13",
        "title": "The Hangover",
        "genre": "Comedy",
        "year": 2009,
        "rating": 7.7,
        "director": "Todd Phillips",
        "duration": "1h 40m",
        "description": "Three buddies wake up from a bachelor party in Las Vegas, with no memory of the previous night and the bachelor missing. They make their way around the city in order to find their friend.",
        "poster_url": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?auto=format&fit=crop&w=800&q=80",
        "cast": "Zach Galifianakis, Bradley Cooper, Ed Helms"
    },
    {
        "item_id": "MOV14",
        "title": "Knives Out",
        "genre": "Comedy",
        "year": 2019,
        "rating": 7.9,
        "director": "Rian Johnson",
        "duration": "2h 10m",
        "description": "A detective investigates the death of a patriarch of an eccentric, combative family in this clever modern murder mystery.",
        "poster_url": "https://images.unsplash.com/photo-1578632767115-351597cf2477?auto=format&fit=crop&w=800&q=80",
        "cast": "Daniel Craig, Chris Evans, Ana de Armas"
    },
    {
        "item_id": "MOV15",
        "title": "Palm Springs",
        "genre": "Comedy",
        "year": 2020,
        "rating": 7.4,
        "director": "Max Barbakow",
        "duration": "1h 30m",
        "description": "Stuck in a time loop, two wedding guests develop a budding romance while living the same day over and over again.",
        "poster_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
        "cast": "Andy Samberg, Cristin Milioti, J.K. Simmons"
    },
    {
        "item_id": "MOV16",
        "title": "La La Land",
        "genre": "Romance",
        "year": 2016,
        "rating": 8.0,
        "director": "Damien Chazelle",
        "duration": "2h 8m",
        "description": "While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations for the future.",
        "poster_url": "https://images.unsplash.com/photo-1485846234645-a62644f84728?auto=format&fit=crop&w=800&q=80",
        "cast": "Ryan Gosling, Emma Stone, Rosemarie DeWitt"
    },
    {
        "item_id": "MOV17",
        "title": "The Notebook",
        "genre": "Romance",
        "year": 2004,
        "rating": 7.8,
        "director": "Nick Cassavetes",
        "duration": "2h 3m",
        "description": "An elderly man reads to a woman with dementia the story of two young lovers who were separated by social differences and reunited decades later.",
        "poster_url": "https://images.unsplash.com/photo-1518895949257-7621c3c786d7?auto=format&fit=crop&w=800&q=80",
        "cast": "Ryan Gosling, Rachel McAdams, James Garner"
    },
    {
        "item_id": "MOV18",
        "title": "About Time",
        "genre": "Romance",
        "year": 2013,
        "rating": 7.8,
        "director": "Richard Curtis",
        "duration": "2h 3m",
        "description": "At the age of 21, Tim discovers he can travel in time and change what happens and has happened in his own life. His decision to make his world a better place by getting a girlfriend turns out not to be so easy.",
        "poster_url": "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?auto=format&fit=crop&w=800&q=80",
        "cast": "Domhnall Gleeson, Rachel McAdams, Bill Nighy"
    },
    {
        "item_id": "MOV19",
        "title": "Pride & Prejudice",
        "genre": "Romance",
        "year": 2005,
        "rating": 7.8,
        "director": "Joe Wright",
        "duration": "2h 9m",
        "description": "Sparks fly when spirited Elizabeth Bennet meets single, rich, and proud Mr. Darcy. But Mr. Darcy reluctantly finds himself falling in love with a woman beneath his class.",
        "poster_url": "https://images.unsplash.com/photo-1469371670807-013ccf25f16a?auto=format&fit=crop&w=800&q=80",
        "cast": "Keira Knightley, Matthew Macfadyen, Brenda Blethyn"
    },
    {
        "item_id": "MOV20",
        "title": "Past Lives",
        "genre": "Romance",
        "year": 2023,
        "rating": 7.9,
        "director": "Celine Song",
        "duration": "1h 45m",
        "description": "Nora and Hae Sung, two deeply connected childhood friends, are wrested apart after Nora's family emigrates from South Korea. Two decades later, they are reunited in New York for one fateful week.",
        "poster_url": "https://images.unsplash.com/photo-1492691527719-9d1e07e534b4?auto=format&fit=crop&w=800&q=80",
        "cast": "Greta Lee, Teo Yoo, John Magaro"
    },
    {
        "item_id": "MOV21",
        "title": "Parasite",
        "genre": "Thriller",
        "year": 2019,
        "rating": 8.5,
        "director": "Bong Joon Ho",
        "duration": "2h 12m",
        "description": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
        "poster_url": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=800&q=80",
        "cast": "Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong"
    },
    {
        "item_id": "MOV22",
        "title": "Se7en",
        "genre": "Thriller",
        "year": 1995,
        "rating": 8.6,
        "director": "David Fincher",
        "duration": "2h 7m",
        "description": "Two detectives, a rookie and a veteran, hunt a serial killer who uses the seven deadly sins as his motives.",
        "poster_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=800&q=80",
        "cast": "Morgan Freeman, Brad Pitt, Kevin Spacey"
    },
    {
        "item_id": "MOV23",
        "title": "Gone Girl",
        "genre": "Thriller",
        "year": 2014,
        "rating": 8.1,
        "director": "David Fincher",
        "duration": "2h 29m",
        "description": "With his wife's disappearance having become the focus of an intense media circus, a man sees the spotlight turned on him when it's suspected that he may not be innocent.",
        "poster_url": "https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&w=800&q=80",
        "cast": "Ben Affleck, Rosamund Pike, Neil Patrick Harris"
    },
    {
        "item_id": "MOV24",
        "title": "Shutter Island",
        "genre": "Thriller",
        "year": 2010,
        "rating": 8.2,
        "director": "Martin Scorsese",
        "duration": "2h 18m",
        "description": "In 1954, a U.S. Marshal investigates the disappearance of a murderer who escaped from a hospital for the criminally insane.",
        "poster_url": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=800&q=80",
        "cast": "Leonardo DiCaprio, Emily Mortimer, Mark Ruffalo"
    },
    {
        "item_id": "MOV25",
        "title": "Zodiac",
        "genre": "Thriller",
        "year": 2007,
        "rating": 7.7,
        "director": "David Fincher",
        "duration": "2h 37m",
        "description": "Between 1968 and 1983, a San Francisco cartoonist becomes an amateur detective obsessed with tracking down the Zodiac Killer.",
        "poster_url": "https://images.unsplash.com/photo-1478760329108-5c3ed9d495a0?auto=format&fit=crop&w=800&q=80",
        "cast": "Jake Gyllenhaal, Robert Downey Jr., Mark Ruffalo"
    }
]

# -------------------------------------------------------------
# 2. MUSIC DATASET
# -------------------------------------------------------------
music_data = [
    {
        "item_id": "MUS01",
        "title": "Blinding Lights",
        "artist": "The Weeknd",
        "album": "After Hours",
        "genre": "Pop",
        "year": 2020,
        "rating": 4.9,
        "duration": "3:20",
        "cover_url": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=800&q=80",
        "vibe": "Upbeat Synthwave"
    },
    {
        "item_id": "MUS02",
        "title": "Levitating",
        "artist": "Dua Lipa",
        "album": "Future Nostalgia",
        "genre": "Pop",
        "year": 2020,
        "rating": 4.8,
        "duration": "3:23",
        "cover_url": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=800&q=80",
        "vibe": "Disco Dance Pop"
    },
    {
        "item_id": "MUS03",
        "title": "Anti-Hero",
        "artist": "Taylor Swift",
        "album": "Midnights",
        "genre": "Pop",
        "year": 2022,
        "rating": 4.7,
        "duration": "3:21",
        "cover_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=800&q=80",
        "vibe": "Moody Electro-Pop"
    },
    {
        "item_id": "MUS04",
        "title": "Shape of You",
        "artist": "Ed Sheeran",
        "album": "÷ (Divide)",
        "genre": "Pop",
        "year": 2017,
        "rating": 4.6,
        "duration": "3:53",
        "cover_url": "https://images.unsplash.com/photo-1498038432885-c6f3f1b912ee?auto=format&fit=crop&w=800&q=80",
        "vibe": "Tropical Pop Rhythm"
    },
    {
        "item_id": "MUS05",
        "title": "Starboy",
        "artist": "The Weeknd ft. Daft Punk",
        "album": "Starboy",
        "genre": "Pop",
        "year": 2016,
        "rating": 4.8,
        "duration": "3:50",
        "cover_url": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=800&q=80",
        "vibe": "Futuristic R&B"
    },
    {
        "item_id": "MUS06",
        "title": "Clair de Lune",
        "artist": "Claude Debussy",
        "album": "Suite Bergamasque",
        "genre": "Classical",
        "year": 1905,
        "rating": 4.9,
        "duration": "5:03",
        "cover_url": "https://images.unsplash.com/photo-1520523839898-5071270409a0?auto=format&fit=crop&w=800&q=80",
        "vibe": "Serene Impressionist Piano"
    },
    {
        "item_id": "MUS07",
        "title": "Experience",
        "artist": "Ludovico Einaudi",
        "album": "In a Time Lapse",
        "genre": "Classical",
        "year": 2013,
        "rating": 4.9,
        "duration": "5:15",
        "cover_url": "https://images.unsplash.com/photo-1465847899084-d164df4dedc6?auto=format&fit=crop&w=800&q=80",
        "vibe": "Cinematic Neoclassical"
    },
    {
        "item_id": "MUS08",
        "title": "Four Seasons: Winter",
        "artist": "Antonio Vivaldi",
        "album": "The Four Seasons",
        "genre": "Classical",
        "year": 1725,
        "rating": 4.8,
        "duration": "8:42",
        "cover_url": "https://images.unsplash.com/photo-1442504028989-ab58b5f29a4a?auto=format&fit=crop&w=800&q=80",
        "vibe": "Dynamic Baroque Violin"
    },
    {
        "item_id": "MUS09",
        "title": "Nuvole Bianche",
        "artist": "Ludovico Einaudi",
        "album": "Una Mattina",
        "genre": "Classical",
        "year": 2004,
        "rating": 4.9,
        "duration": "5:57",
        "cover_url": "https://images.unsplash.com/photo-1518609878373-06d740f60d8b?auto=format&fit=crop&w=800&q=80",
        "vibe": "Emotional Solitary Piano"
    },
    {
        "item_id": "MUS10",
        "title": "Moonlight Sonata (Adagio)",
        "artist": "Ludwig van Beethoven",
        "album": "Piano Sonata No. 14",
        "genre": "Classical",
        "year": 1801,
        "rating": 4.9,
        "duration": "6:05",
        "cover_url": "https://images.unsplash.com/photo-1507838153414-b4b713384a76?auto=format&fit=crop&w=800&q=80",
        "vibe": "Poignant Classical Masterpiece"
    },
    {
        "item_id": "MUS11",
        "title": "Lose Yourself",
        "artist": "Eminem",
        "album": "8 Mile Soundtrack",
        "genre": "Hip-Hop",
        "year": 2002,
        "rating": 4.9,
        "duration": "5:26",
        "cover_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=800&q=80",
        "vibe": "Energetic Motivational Rap"
    },
    {
        "item_id": "MUS12",
        "title": "HUMBLE.",
        "artist": "Kendrick Lamar",
        "album": "DAMN.",
        "genre": "Hip-Hop",
        "year": 2017,
        "rating": 4.8,
        "duration": "2:57",
        "cover_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?auto=format&fit=crop&w=800&q=80",
        "vibe": "Hard-Hitting Heavy Bass"
    },
    {
        "item_id": "MUS13",
        "title": "God's Plan",
        "artist": "Drake",
        "album": "Scorpion",
        "genre": "Hip-Hop",
        "year": 2018,
        "rating": 4.7,
        "duration": "3:18",
        "cover_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=800&q=80",
        "vibe": "Catchy Melodic Trap"
    },
    {
        "item_id": "MUS14",
        "title": "Sicko Mode",
        "artist": "Travis Scott",
        "album": "Astroworld",
        "genre": "Hip-Hop",
        "year": 2018,
        "rating": 4.8,
        "duration": "5:12",
        "cover_url": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=800&q=80",
        "vibe": "Psychedelic Multi-Beat Rap"
    },
    {
        "item_id": "MUS15",
        "title": "Alright",
        "artist": "Kendrick Lamar",
        "album": "To Pimp a Butterfly",
        "genre": "Hip-Hop",
        "year": 2015,
        "rating": 4.9,
        "duration": "3:39",
        "cover_url": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=800&q=80",
        "vibe": "Jazz Rap Anthem"
    },
    {
        "item_id": "MUS16",
        "title": "Bohemian Rhapsody",
        "artist": "Queen",
        "album": "A Night at the Opera",
        "genre": "Rock",
        "year": 1975,
        "rating": 5.0,
        "duration": "5:55",
        "cover_url": "https://images.unsplash.com/photo-1465847899084-d164df4dedc6?auto=format&fit=crop&w=800&q=80",
        "vibe": "Operatic Classic Rock"
    },
    {
        "item_id": "MUS17",
        "title": "Sweet Child O' Mine",
        "artist": "Guns N' Roses",
        "album": "Appetite for Destruction",
        "genre": "Rock",
        "year": 1987,
        "rating": 4.8,
        "duration": "5:56",
        "cover_url": "https://images.unsplash.com/photo-1498038432885-c6f3f1b912ee?auto=format&fit=crop&w=800&q=80",
        "vibe": "Hard Rock Guitar Riff"
    },
    {
        "item_id": "MUS18",
        "title": "In the End",
        "artist": "Linkin Park",
        "album": "Hybrid Theory",
        "genre": "Rock",
        "year": 2000,
        "rating": 4.9,
        "duration": "3:36",
        "cover_url": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=800&q=80",
        "vibe": "Nu Metal Emotional Rock"
    },
    {
        "item_id": "MUS19",
        "title": "Hotel California",
        "artist": "Eagles",
        "album": "Hotel California",
        "genre": "Rock",
        "year": 1976,
        "rating": 4.9,
        "duration": "6:30",
        "cover_url": "https://images.unsplash.com/photo-1520523839898-5071270409a0?auto=format&fit=crop&w=800&q=80",
        "vibe": "Legendary Solo Rock"
    },
    {
        "item_id": "MUS20",
        "title": "Back in Black",
        "artist": "AC/DC",
        "album": "Back in Black",
        "genre": "Rock",
        "year": 1980,
        "rating": 4.8,
        "duration": "4:15",
        "cover_url": "https://images.unsplash.com/photo-1442504028989-ab58b5f29a4a?auto=format&fit=crop&w=800&q=80",
        "vibe": "Thunderous Heavy Rock"
    },
    {
        "item_id": "MUS21",
        "title": "Someone Like You",
        "artist": "Adele",
        "album": "21",
        "genre": "Melody",
        "year": 2011,
        "rating": 4.9,
        "duration": "4:45",
        "cover_url": "https://images.unsplash.com/photo-1518609878373-06d740f60d8b?auto=format&fit=crop&w=800&q=80",
        "vibe": "Soulful Heartbreak Ballad"
    },
    {
        "item_id": "MUS22",
        "title": "Perfect",
        "artist": "Ed Sheeran",
        "album": "÷ (Divide)",
        "genre": "Melody",
        "year": 2017,
        "rating": 4.8,
        "duration": "4:23",
        "cover_url": "https://images.unsplash.com/photo-1507838153414-b4b713384a76?auto=format&fit=crop&w=800&q=80",
        "vibe": "Romantic Acoustic Melody"
    },
    {
        "item_id": "MUS23",
        "title": "Fix You",
        "artist": "Coldplay",
        "album": "X&Y",
        "genre": "Melody",
        "year": 2005,
        "rating": 4.9,
        "duration": "4:55",
        "cover_url": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=800&q=80",
        "vibe": "Uplifting Emotional Melody"
    },
    {
        "item_id": "MUS24",
        "title": "All of Me",
        "artist": "John Legend",
        "album": "Love in the Future",
        "genre": "Melody",
        "year": 2013,
        "rating": 4.8,
        "duration": "4:29",
        "cover_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=800&q=80",
        "vibe": "Soulful Piano Serenade"
    },
    {
        "item_id": "MUS25",
        "title": "Stay With Me",
        "artist": "Sam Smith",
        "album": "In the Lonely Hour",
        "genre": "Melody",
        "year": 2014,
        "rating": 4.7,
        "duration": "2:52",
        "cover_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?auto=format&fit=crop&w=800&q=80",
        "vibe": "Gospel-Infused Ballad"
    }
]

# -------------------------------------------------------------
# 3. SHOPPING PRODUCTS DATASET
# -------------------------------------------------------------
products_data = [
    {
        "item_id": "PROD01",
        "name": "Sony WH-1000XM5 ANC Headphones",
        "category": "Electronics",
        "price": 399.99,
        "rating": 4.8,
        "brand": "Sony",
        "discount": "15% OFF",
        "specs": "Industry-leading noise cancellation, 30hr battery, Hi-Res Audio",
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80"
    },
    {
        "item_id": "PROD02",
        "name": "Apple MacBook Air 15\" M3",
        "category": "Electronics",
        "price": 1299.00,
        "rating": 4.9,
        "brand": "Apple",
        "discount": "8% OFF",
        "specs": "Apple M3 Chip, Liquid Retina display, 18hr battery, 16GB RAM",
        "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=800&q=80"
    },
    {
        "item_id": "PROD03",
        "name": "Samsung Galaxy S24 Ultra 512GB",
        "category": "Electronics",
        "price": 1199.99,
        "rating": 4.7,
        "brand": "Samsung",
        "discount": "10% OFF",
        "specs": "Snapdragon 8 Gen 3, Titanium frame, 200MP camera, S-Pen included",
        "image_url": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?auto=format&fit=crop&w=800&q=80"
    },
    {
        "item_id": "PROD04",
        "name": "iPad Pro 11\" M4 OLED",
        "category": "Electronics",
        "price": 999.00,
        "rating": 4.8,
        "brand": "Apple",
        "discount": "5% OFF",
        "specs": "Tandem OLED Ultra Retina XDR, M4 chip, 5.3mm ultra-thin design",
        "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&w=800&q=80"
    },
    {
        "item_id": "PROD05",
        "name": "Dell UltraSharp 32\" 4K USB-C Monitor",
        "category": "Electronics",
        "price": 749.50,
        "rating": 4.6,
        "brand": "Dell",
        "discount": "12% OFF",
        "specs": "IPS Black technology, 98% DCI-P3 color accuracy, 90W power delivery",
        "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=800&q=80"
    },
    {
        "item_id": "PROD06",
        "name": "Sony PlayStation 5 Pro Console",
        "category": "Electronics",
        "price": 699.99,
        "rating": 4.8,
        "brand": "Sony",
        "discount": "Limited Stock",
        "specs": "Advanced ray tracing, AI upscaling PSSR, 2TB SSD storage",
        "image_url": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?auto=format&fit=crop&w=800&q=80"
    },
    {
        "item_id": "PROD07",
        "name": "Classic Genuine Leather Biker Jacket",
        "category": "Fashion",
        "price": 249.00,
        "rating": 4.7,
        "brand": "AllSaints",
        "discount": "20% OFF",
        "specs": "100% lambskin leather, asymmetric zip, quilted lining, tailored fit",
        "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=800&q=80"
    },
    {
        "item_id": "PROD08",
        "name": "Italian Merino Wool Slim-fit Blazer",
        "category": "Fashion",
        "price": 320.00,
        "rating": 4.8,
        "brand": "Hugo Boss",
        "discount": "15% OFF",
        "specs": "Breathable 100% virgin wool, notched lapels, two-button silhouette",
        "image_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=800&q=80"
    },
    {
        "item_id": "PROD09",
        "name": "Japanese Raw Selvedge Denim Jeans",
        "category": "Fashion",
        "price": 165.00,
        "rating": 4.5,
        "brand": "Naked & Famous",
        "discount": "10% OFF",
        "specs": "14oz shuttle-loomed Japanese denim, unwashed indigo, custom copper rivets",
        "image_url": "https://images.unsplash.com/photo-1542272604-780c96856592?auto=format&fit=crop&w=800&q=80"
    },
    {
        "item_id": "PROD10",
        "name": "Nike Air Jordan 1 Retro High OG",
        "category": "Fashion",
        "price": 180.00,
        "rating": 4.9,
        "brand": "Nike",
        "discount": "Popular Pick",
        "specs": "Iconic colorway, premium full-grain leather, encapsulated Air cushioning",
        "image_url": "https://images.unsplash.com/photo-1552346154-21d32810aba3?auto=format&fit=crop&w=800&q=80"
    },
    {
        "item_id": "PROD11",
        "name": "Pure Cashmere Knit Crewneck Sweater",
        "category": "Fashion",
        "price": 195.00,
        "rating": 4.7,
        "brand": "Everlane",
        "discount": "18% OFF",
        "specs": "Grade-A Mongolian cashmere, ribbed cuffs and hem, ultra-soft handfeel",
        "image_url": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?auto=format&fit=crop&w=800&q=80"
    },
    {
        "item_id": "PROD12",
        "name": "Waterproof Technical Urban Trench",
        "category": "Fashion",
        "price": 280.00,
        "rating": 4.6,
        "brand": "Arc'teryx Veilance",
        "discount": "12% OFF",
        "specs": "GORE-TEX 3-layer weatherproof shell, taped seams, concealed magnetic storm flap",
        "image_url": "https://images.unsplash.com/photo-1544441893-675973e31985?auto=format&fit=crop&w=800&q=80"
    },
    {
        "item_id": "PROD13",
        "name": "Fossil Heritage Automatic Watch",
        "category": "Accessories",
        "price": 280.00,
        "rating": 4.6,
        "brand": "Fossil",
        "discount": "25% OFF",
        "specs": "Exhibition caseback, automatic self-winding movement, stainless steel bracelet",
        "image_url": "https://images.unsplash.com/photo-1524805444758-089113d48a6d?auto=format&fit=crop&w=800&q=80"
    },
    {
        "item_id": "PROD14",
        "name": "Ray-Ban Classic Polarized Wayfarer",
        "category": "Accessories",
        "price": 185.00,
        "rating": 4.7,
        "brand": "Ray-Ban",
        "discount": "15% OFF",
        "specs": "Crystal green polarized lenses, 100% UV protection, durable acetate frame",
        "image_url": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=800&q=80"
    },
    {
        "item_id": "PROD15",
        "name": "Bellroy Slim Leather Bi-fold Wallet",
        "category": "Accessories",
        "price": 89.00,
        "rating": 4.8,
        "brand": "Bellroy",
        "discount": "Best Seller",
        "specs": "Holds 4-12 cards + flat bills, certified environmentally tanned leather, RFID protection",
        "image_url": "https://images.unsplash.com/photo-1627123424574-724758594e93?auto=format&fit=crop&w=800&q=80"
    },
    {
        "item_id": "PROD16",
        "name": "Peak Design Everyday Backpack 30L",
        "category": "Accessories",
        "price": 279.95,
        "rating": 4.9,
        "brand": "Peak Design",
        "discount": "Editor's Choice",
        "specs": "Weatherproof 400D nylon canvas, MagLatch hardware, FlexFold internal dividers",
        "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=800&q=80"
    },
    {
        "item_id": "PROD17",
        "name": "Apple Watch Ultra 2 GPS + Cellular",
        "category": "Accessories",
        "price": 799.00,
        "rating": 4.9,
        "brand": "Apple",
        "discount": "Top Rated",
        "specs": "49mm rugged aerospace titanium case, 3000-nit screen, dual-frequency precision GPS",
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80"
    },
    {
        "item_id": "PROD18",
        "name": "Samsonite Proxis Hardside Spinner Luggage",
        "category": "Accessories",
        "price": 420.00,
        "rating": 4.7,
        "brand": "Samsonite",
        "discount": "20% OFF",
        "specs": "Roxkin multi-layered shock-absorbing shell, dual-caster smooth wheels, TSA lock",
        "image_url": "https://images.unsplash.com/photo-1565026057447-bc90a3dceb87?auto=format&fit=crop&w=800&q=80"
    },
    {
        "item_id": "PROD19",
        "name": "De'Longhi Magnifica S Espresso Machine",
        "category": "Home Appliances",
        "price": 649.95,
        "rating": 4.8,
        "brand": "De'Longhi",
        "discount": "16% OFF",
        "specs": "Bean-to-cup conical burr grinder, 15-bar pressure pump, manual milk frothing wand",
        "image_url": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?auto=format&fit=crop&w=800&q=80"
    },
    {
        "item_id": "PROD20",
        "name": "Dyson V15 Detect Cordless Vacuum",
        "category": "Home Appliances",
        "price": 749.99,
        "rating": 4.9,
        "brand": "Dyson",
        "discount": "10% OFF",
        "specs": "Laser reveals microscopic dust, piezo sensor measures particle size, 60min runtime",
        "image_url": "https://images.unsplash.com/photo-1558317374-067fb5f30001?auto=format&fit=crop&w=800&q=80"
    },
    {
        "item_id": "PROD21",
        "name": "Philips Airfryer XXL Smart Sensing 7.2L",
        "category": "Home Appliances",
        "price": 229.00,
        "rating": 4.7,
        "brand": "Philips",
        "discount": "22% OFF",
        "specs": "Twin TurboStar fat-removal technology, digital touchscreen, dishwasher-safe basket",
        "image_url": "https://images.unsplash.com/photo-1585515320310-259814833e62?auto=format&fit=crop&w=800&q=80"
    },
    {
        "item_id": "PROD22",
        "name": "Le Creuset Enameled Cast Iron Dutch Oven",
        "category": "Home Appliances",
        "price": 420.00,
        "rating": 4.9,
        "brand": "Le Creuset",
        "discount": "Lifetime Warranty",
        "specs": "5.5-quart capacity, superior heat retention, vibrant chip-resistant exterior enamel",
        "image_url": "https://images.unsplash.com/photo-1584269600464-37b1b58a9fe7?auto=format&fit=crop&w=800&q=80"
    },
    {
        "item_id": "PROD23",
        "name": "KitchenAid Artisan Stand Mixer 5-Qt",
        "category": "Home Appliances",
        "price": 449.99,
        "rating": 4.8,
        "brand": "KitchenAid",
        "discount": "Iconic Kitchen Pick",
        "specs": "10 optimized speeds, tilt-head design, includes flat beater, dough hook, wire whip",
        "image_url": "https://images.unsplash.com/photo-1594385208974-2e75f8d7bb48?auto=format&fit=crop&w=800&q=80"
    },
    {
        "item_id": "PROD24",
        "name": "Dyson Purifier Hot+Cool Gen1 HP10",
        "category": "Home Appliances",
        "price": 499.00,
        "rating": 4.6,
        "brand": "Dyson",
        "discount": "14% OFF",
        "specs": "3-in-1 HEPA H13 air purifier, rapid space heater, and cooling fan with Air Multiplier",
        "image_url": "https://images.unsplash.com/photo-1585338107529-13afc5f02586?auto=format&fit=crop&w=800&q=80"
    },
    {
        "item_id": "PROD25",
        "name": "Brevillle Barista Touch Espresso Machine",
        "category": "Home Appliances",
        "price": 999.95,
        "rating": 4.8,
        "brand": "Breville",
        "discount": "Barista Grade",
        "specs": "Automated touchscreen menu, ThermoJet 3-sec heatup, automated microfoam texturing",
        "image_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=800&q=80"
    }
]

# Save catalogs as CSV
pd.DataFrame(movies_data).to_csv("data/movies.csv", index=False)
pd.DataFrame(music_data).to_csv("data/music.csv", index=False)
pd.DataFrame(products_data).to_csv("data/products.csv", index=False)
print("Saved catalog CSV files.")

# -------------------------------------------------------------
# 4. GENERATE REALISTIC USER RATINGS MATRICES (15 Users)
# -------------------------------------------------------------
# We'll define specific taste personas for Users 1 to 5,
# and structured random/persona patterns for Users 6 to 15.

users = [f"User_{i}" for i in range(1, 16)]

# Genre affinities for archetypes:
# Persona 1: Sci-Fi, Action / Rock, Hip-Hop / Electronics
# Persona 2: Romance, Comedy / Pop, Melody / Fashion, Accessories
# Persona 3: Thriller, Sci-Fi / Classical, Melody / Home Appliances, Electronics
# Persona 4: Action, Thriller / Hip-Hop, Rock / Accessories, Fashion
# Persona 5: All-rounder high-critic cinephile & audiophile

def generate_ratings(items_df, category_col, item_id_col, user_personas):
    records = []
    np.random.seed(42)
    
    for u_idx, user in enumerate(users):
        persona = user_personas[u_idx % len(user_personas)]
        
        # Decide how many items this user rates (between 10 and 16 out of 25)
        num_rated = np.random.randint(11, 17)
        # Weight item selection based on affinity
        weights = []
        base_scores = []
        for _, row in items_df.iterrows():
            cat = row[category_col]
            affinity = persona.get(cat, 0.5) # affinity from 0.1 to 1.0
            weights.append(affinity)
            # base score centered around affinity * 5
            expected_rating = 1.0 + (affinity * 4.0)
            base_scores.append(expected_rating)
            
        weights = np.array(weights)
        weights /= weights.sum()
        
        chosen_indices = np.random.choice(len(items_df), size=num_rated, replace=False, p=weights)
        
        for idx in chosen_indices:
            row = items_df.iloc[idx]
            mean_score = base_scores[idx]
            # Add gaussian noise
            rating = np.round(np.random.normal(mean_score, 0.4) * 2) / 2 # rounds to nearest 0.5
            rating = max(1.0, min(5.0, rating))
            records.append({
                "user_id": user,
                "item_id": row[item_id_col],
                "rating": rating
            })
            
    return pd.DataFrame(records)

# Personas definition:
movie_personas = [
    {"Sci-Fi": 0.95, "Action": 0.90, "Thriller": 0.70, "Comedy": 0.30, "Romance": 0.20}, # User 1 (Action/Sci-Fi)
    {"Romance": 0.95, "Comedy": 0.90, "Sci-Fi": 0.20, "Action": 0.30, "Thriller": 0.40}, # User 2 (Romance/Comedy)
    {"Thriller": 0.95, "Sci-Fi": 0.85, "Romance": 0.60, "Comedy": 0.40, "Action": 0.50}, # User 3 (Mind-bender Thrillers)
    {"Action": 0.95, "Comedy": 0.80, "Thriller": 0.75, "Sci-Fi": 0.60, "Romance": 0.30}, # User 4 (Blockbuster Action)
    {"Sci-Fi": 0.80, "Thriller": 0.85, "Romance": 0.80, "Comedy": 0.80, "Action": 0.80}, # User 5 (Balanced Cinephile)
]

music_personas = [
    {"Rock": 0.95, "Hip-Hop": 0.90, "Pop": 0.50, "Melody": 0.30, "Classical": 0.40}, # User 1
    {"Pop": 0.95, "Melody": 0.90, "Hip-Hop": 0.60, "Rock": 0.30, "Classical": 0.40}, # User 2
    {"Classical": 0.98, "Melody": 0.90, "Rock": 0.40, "Pop": 0.30, "Hip-Hop": 0.20}, # User 3
    {"Hip-Hop": 0.95, "Rock": 0.85, "Pop": 0.70, "Classical": 0.20, "Melody": 0.30}, # User 4
    {"Melody": 0.85, "Classical": 0.85, "Rock": 0.80, "Pop": 0.80, "Hip-Hop": 0.70}, # User 5
]

product_personas = [
    {"Electronics": 0.98, "Accessories": 0.70, "Fashion": 0.35, "Home Appliances": 0.40}, # User 1
    {"Fashion": 0.95, "Accessories": 0.90, "Home Appliances": 0.60, "Electronics": 0.30}, # User 2
    {"Home Appliances": 0.98, "Electronics": 0.75, "Accessories": 0.60, "Fashion": 0.30}, # User 3
    {"Accessories": 0.95, "Fashion": 0.85, "Electronics": 0.70, "Home Appliances": 0.40}, # User 4
    {"Electronics": 0.85, "Home Appliances": 0.85, "Fashion": 0.75, "Accessories": 0.80}, # User 5
]

movie_ratings_df = generate_ratings(pd.DataFrame(movies_data), "genre", "item_id", movie_personas)
music_ratings_df = generate_ratings(pd.DataFrame(music_data), "genre", "item_id", music_personas)
product_ratings_df = generate_ratings(pd.DataFrame(products_data), "category", "item_id", product_personas)

movie_ratings_df.to_csv("data/movie_ratings.csv", index=False)
music_ratings_df.to_csv("data/music_ratings.csv", index=False)
product_ratings_df.to_csv("data/product_ratings.csv", index=False)

print(f"Generated {len(movie_ratings_df)} movie ratings, {len(music_ratings_df)} music ratings, {len(product_ratings_df)} product ratings.")

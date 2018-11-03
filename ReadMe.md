### Data Science Project
Motivation: See if the amount of traction words
have on urban dictionary have any bearing on their
popularity on other social media platforms. 

Extention: Could words popular in news articles have any
effect on on viewship of social media posts?

#### Reason
Urban dictionary tends to have words that are more used
in current parlance be upvoted. Social media posts containing
these words may be more likley to grab viewer attention.
Similarly news articles tend to introduce vocabulary people
care about, so does using this vocabulary in our own
social media increase viewership. 

Initially was going to use zdict to get words, instead
used data available on reddit. File to parse json is
current and benchmarked with various implementations 
of JSON to SQLite in python. Most current solution
runs on a 1.6GB file in under a minute on my laptop.
Example of parsed file is included under data.
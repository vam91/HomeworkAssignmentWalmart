# HomeworkAssignmentWalmart

* ## Implement a data pipeline, using your programming language of choice, that outputs a machine-learning ready dataset. ##
  * ### Connect to the Twitter streaming API and do a keyword search on Justin Bieber: ###
      * Twitter API V2 Filtered Streaming was used. A rule was set that looked for Tweets having the keyword 'Justin Bieber', and then a requests stream is initiated to start pulling tweets from that stream.
  * ### Filter out all tweets having to do with music: ###
      * The filtered stream rule also includes a context annotation to NOT include any tweets having to do with 'Music Album' operator: -context:89.*. Twitter annotates a percentage of their tweets with a context [Link](https://developer.twitter.com/en/docs/twitter-api/annotations/faq). This is flawed as a large percentage of tweets do not recieve an annotation, but does provide a simple way to determine if a tweet is talking about music or not. There is also context:54 (Musician) and context:84 (Book Music Genre), but these contexts are accepted as the volume of tweets was too low.
  * ### Store the tweets into a database of your choosing: ###   
    * Pandas and SQL Alchemy Engine were used to load tweets into a SQL Server database. SQL Scripts to generate the final Tables and Views are attached. 
    * #### Avoid duplicates ####  
        * Duplicates were defind as retweets. Retweets are a fully copy of the original tweet with no added content. Quoted Tweets however, are a retweet with some additional content added by the person retweeting. Retweets are filtered out due to the -is:retweet operator (the dash is used to negate)
    * #### Produce a count of all tweets consumed ####
     * Count of tweets consumed/loaded is available in the vw_tweets SQL view. Please reference the SQL_Scripts file for the view's SQL code.
    * #### Produce a count of unique tweets ####
     * Only unique tweets are consumed/loaded into DB. This solution leverages Twitter's API to filter out duplicates (aka retweets)
  * Save all code in a GitHub repo and share the link with us
* ## Answer the following: ##
    * ### What are the risks involved in building such a pipeline? ###  
        * This is not a scaleable solution. If Justin Bieber starts trending, then this solution would struggle to handle the increase in volume. I do not have much experience working with Streaming data/pipelines, but tools such as pyspark, kafka, and/or a NOSQL DB (don't have to worry about table/column mapping) would help in making the solution more sustainable at high work loads.
        * The methodology needs to be really refined and vetted. Current solution has a large dependency on Twitter's context annotation system, and Twitter does not annotate a large percentage of tweets; so many tweets are not getting evaluated. Additionally, there is no transparency on how Twitter is generating the annotations; it would be difficult/impossible to explain to data stakeholders/clients on why a tweet was or was not annotated under the 'Music' category.
    * ### How would you roll out the pipeline going from proof-of-concept to a production-ready solution? ###
      * Refine methodology around what tweets to capture and discard
      * Setup an infrastructure to start the ETL/ELT pipeline. Identify which tools to perform the Extract, Transforming, and Loading. Setup error handling, automated retries (in case of minor errors, timeouts, etc.), and unit tests
      * Setup logging and notification system
      * Test this solution, and refine the methodology; also address any bug fixes
      * Deploy to production
      * #### What would a production-ready solution entail that a POC wouldn't? ####
        * Refined and an agreed-upon methodology of what tweets to capture
        * Cleaned and prepped dataset (e.g. production views/tables) for consumption by data stakeholders
        * A thorough logging and notification/alert system
      * #### What is the level of effort required to deliver each phase of the solution? ####
        * Refining Methodology - 2 weeks to clarify requirements ('Music related tweets' is an open-ended definition), test (are there music related tweets still being captured), bug-fix/refinement
        * Setting up infrastructure - 2 weeks; 1 week for infrastructure setup and testing 1 week for ETL/ELT setup and testing. (logging, alert system, and unit tests included in 2 week estimate)
      * #### What is your estimated timeline for delivery for a production-ready solution? ####
        * ~4 weeks
        * This timeline can be flexed shorter or longer depending on deadlines. The methodology refinement phase can be as complicated or simple as the timeline would allow. 

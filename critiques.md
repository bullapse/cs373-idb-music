**What did they do well?**
collegedb.me is a very nicely designed website. The front end design and color scheme is very fitting for the website. For the population of the page, it is very fluid and all rendered in the same page for each pillar and the pagination seems to use dynamic loading using something like AngularJS. The universities details pages are well made and provide useful info, the maps API integration is impressive too.

**What can they do better?**
For the list pages, it seems like they just populate the rows with data from each of the objects and might have been nicer to represent those fields with something other than just raw data. The states details pages are fairly plain and the list of universities are a little under represented on the page.The degrees details pages have the same problem, it's fairly plain and only lists universities in an unmeaningful way. During the rendering of each degree detail page as well, the query for the universities seems to load all of them at once and results in the list being populated noticeably later than everything else. For this, paging in the back end might have been useful.

**What did we learn from their website?**
Looking at their website, it definitely looks like we should have spent more time on the front end of our website. We also could have refined our page population to be dynamic since it feels much cleaner on their site. Using AngularJS along with Flask would have made our site cleaner and functional based on their site. Our details pages do seem a little more comprehensive and useful though.

**What puzzles us about their website?**
We wondered why there wasn't much useful representation of the data that they collected. The layout and design of the web app is very slick but when it comes to the tables and details pages, it seems a little plain. There was definitely experience in front end so we wondered why they didn't use that to creatively display data.



**What did we do well?**
For our website, we displayed the data that we collected in a creative and meaningful manner. Users can browse through artists, albums, and tracks and see everything they need to on each of them. For tracks we even included previews of the tracks. The progress bar for popularity is a good visual indicator that a user can quickly glance at and comprehend. For our back-end, we set it up in a way that would make it future proof. For the data retrieval for the front end, we had the pagination occur in the back end so that there would be no delay in populating the front end which would really come into use for a very large amount of data. For our data models, we did a good job of creating associations between each class so that links could be very easily found between objects

**What can we do better?**
We could have spent more effort on the front end and making the layout and colors blend together a little more or make it a little softer. As it is, our design for our website seems a little mismatched. Unfortunately for our back end we didn't populate our database with that many objects so we didn't see the benefits of the work we put into the back-end.

**What did we learn?**
One thing we learned is to plan which frameworks and libraries to use ahead of time instead of trying to integrating whatever we find when we need it. We had some problems trying to use certain libraries that wouldn't work with the ones that we already had without in depth special configuration. We also learned that we need to communicate exactly what we were working on to avoid duplicate work. We realized that we should probably start on projects as soon as possible so that we aren't working all day that it's due.

**What puzzles us?**
We are a little concerned about the actual use cases of our web app. It looks nice and provides useful info for songs that we have but aside from that we kind of wonder when anyone would use it as opposed to Spotify, especially with the name.

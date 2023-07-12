Service description

Allows CRUD operations for Povider and ServiceArea models.

Allows checking whether a point with a given lat and long belongs to any ServiceArea.

Runs on AWS EC2 t2.micro with elastic IP and AWS RDS db.t3.micro with POSTgis.

Host address: 52.215.199.77:8000

API documentation: http://52.215.199.77:8000/docs/

Initially i wanted to deploy it via AWS ElasticBeanstalk, but it required building the libraries required for geoDjango from source, since it uses amazon linux. And t2.micro ran out of memory while building PROJ4 (trying to keep it free tier). So i switched to manual EC2 configuration. But you can check out the progress in .ebextensions, i am sure it could be done on a bigger instance or with some docker deployment.

Not sure on the requirements for the speed required for the "point in polygons" search, but some optimizations come to mind, like - https://www.alibabacloud.com/blog/optimize-spatial-searches-in-postgresql-using-st-contains-and-st-within_597192. But i think this is not in the scope of a test task.

I know the serializer and view names dont follow the CamelCase, just a prefference, but i am up to whatever style is required.





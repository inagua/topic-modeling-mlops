# Amazon Web Services 
## Comparison - EC2 vs EKS vs SageMaker


| Services  | Cost      |
|-----------|---------  |
| EC2       | 207.83$   |
| EKS       | 219.00$   |
| SageMaker | 3,630.00$ |



https://calculator.aws/#/

* **<u>Cost</u>**:
    * <u>*Minimum system requirements*</u>:
        * eu-west-3 (Europe Paris)
        * 3 instances
        * 750h/month
        * Quick Estimation
        * Linux 
        * 4 CPU 
        * 50 GB storage
        * 12 GB memory
        * Utilisations: 100 utilisations/month
    * <u>EC2</u>: 3 instances x 0,0949 USD x 730 heures dans le mois = 207,83 USD
    * <u>EKS</u>: 3 Clusters x 0,10 USD par heure x 730 heures par mois = 219,00 USD
    * <u>SageMaker</u>: 100 scientifique(s) des données x 3 Instances de bloc-notes Studio = 300,00 Instances de bloc-notes Studio
300,00 Instances de bloc-notes Studio x 10 heures par jour x 5 jours par mois = 15 000,00 Heures SageMaker Studio Notebook par mois
15 000,00 heures par mois x 0,242 USD coût d'instance par heure = 3 630,00 USD

* <u>**Pros and Cons**</u>:
    * <u>EC2</u>: 
        * (+) Cost
        * (+) Cluster portability - custom k8s cluster
        * (+) Easy to move workloads to a different environment, such as on-premises
        * (-) Technical complexities of k8s architecture in order for workloads to run as expected once deployed
        * (-) Implementation
        * (-) Management
        * (-) Need multiple machine/cluster
    * <u>EKS</u>:
        * (+) High performance
        * (+) Minimal management 
        * (+) Integration with AWS Services
        * (+) Autoscaling
        * (+) Cost
        * (+) Great for K8s cluster | Open- source support
        * (+) AWS network - VPN plugin
        * (-) Need other services to store and manage user accounts - Authentification
        * (-) Complex set of architectural components
    * <u>SageMaker</u>:
        + (+) Implementation
        + (+) Model monitoring
        + (+) Control and scale environment effortlessly
        + (+) Great for MLOps 
        + (+) Getting charged when active
        - (-) Cost astronomical
        - (-) Customization

**<u>ressources:</u>**
* https://resources.experfy.com/ai-ml/scaling-machine-learning-from-0-to-millions-of-users-part-2-training-ec2-emr-ecs-eks-or-sagemaker/
* https://www.cloudforecast.io/blog/ecs-vs-eks/

### More Services to take advantage of AWS 

| Services   | Cost |
|------------|------|
| S3  | 12.42$ |
| RDS (PostgreSQL) |  ~133.00$ |
| Cognito | ~514,25$ |

* Information cost: 
    * 500Go
    * 20 000 query 
    * 10000 users (UAM - Cognito)





***


# Deploy and Manage Kubeflow on AWS EKS (test -> see later) 

This is a demo to deploy and manage Kubeflow on AWS EKS. 
https://github.com/data-science-on-aws/data-science-on-aws

## Prerequisites
1. AWS account
2. EKS Cluster 
3. SageMaker Studio 


### SageMaker 
SageMaker is AWS’s fully managed, end-to-end platform covering the entire ML workflow within many frameworks. 

* Jupyter notebook instances 
* High performance algorithms 
* Large-scale training
* Optimization
* One-click deployment
* Fully managed with auto-scaling

### <u>*Notes (for me) in kubeflow (?) *</u>
* Tensor RT - model deployment 
* Katib - Hyper-param-tuning 


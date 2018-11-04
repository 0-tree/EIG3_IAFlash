
.. markdown version of this readme here: https://github.com/jehna/readme-best-practices/blob/master/README-default.md


.. image:: logo.png
    :width: 200px
    :align: center
    :height: 100px


EIG3_IAFlash - Car Model Detection
==================================

  Preventing the burden of false contraventions by detecting cars models in radar snapshots.

| This project acts as a simple showcase of ideas for the `AIFlash <https://entrepreneur-interet-general.etalab.gouv.fr/defis/2019/iaflash.html>`_ project (*November 2018*).
| It can also be seen as an overview of possible work when dealing with **images**, and here specifically car model detection.


Features
++++++++


As such, this project shows examples of:

- downloading and processing data from an existing open dataset
- using transfer learning to classify cars from labelled data
- using expert-crafted feature extraction and clustering to label unlabelled data
- scrapping web sources to build a custom labelled dataset 

| Each example is treated in a dedicated Jupyter notebook in the ``IAFlash`` directory.
| Please note that given the short amount of time available, these notebooks should be considered as *examples* and not a final product.


A short presentation is also available `here <https://slides.com/tree_0/iaflash/>`_.


Roadmap
+++++++


To do
-----

.. nested lists must have a line space between parent and child

- improve performances


Processing
----------

None.


Done
----

- literature review 
- handling the  `cars <http://ai.stanford.edu/~jkrause/cars/car_dataset.html>`_ dataset
- try transfer learning
- try 'classical' feature extractors and image clustering
- try web scrapping
- cleanup


References
++++++++++

Data
----

- we work on an `open car dataset <http://ai.stanford.edu/~jkrause/cars/car_dataset.html>`_ from Stanford.

- other potential sources:

  - `CompCar <http://mmlab.ie.cuhk.edu.hk/datasets/comp_cars/index.html>`_ dataset (needs to contact the authors).


Pre-trained models
------------------

- we use some of the models from the Keras `model zoo <https://keras.io/applications/>`_ (trained on ImageNet).


Licensing
+++++++++

The code in this project is licensed under GNU General Public License v3.0.


.. END
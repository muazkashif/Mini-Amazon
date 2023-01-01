Code for the final project of COMPSCI 316: Database Systems


This app is optimized for the class VM.
If you have a different setup, your mileage with the following instructions may vary.

## Installing the Project

1. Fork this repo by clicking the small 'Fork' button at the very top right on Gitlab.
2. In your newly forked repo, find the blue "Clone" button.
   Copy the "Clone with SSH" text.
   In your terminal on the VM, you can now issue the command `git clone THE_TEXT_YOU_JUST_COPIED`.
   Make sure to replace 'THE_TEXT_YOU_JUST_COPIED' with the "Clone with SSH" text.
3. In your VM, change into the repository directory and then run `./install.sh`.
   This will install a bunch of things, set up an important file called `.flashenv`, and creates a simple PostgreSQL database named `amazon`.
4. If you are running a Google VM, to view the app in your browser, you may need to edit the firewall rules.
   The [Google VM instructions](https://courses.cs.duke.edu/fall22/compsci316d/instructions/gcp/) on the course page has instructions for how to add rules at the bottom.
   If those for some reason are outdated, here are [instructions provided by Google](https://cloud.google.com/vpc/docs/using-firewalls).
   Create a rule to open up port 5000, which flask will run on.

## Running/Stopping the Website

To run the website, in your VM, go into the repository directory and issue the following commands:
```
source env/bin/activate
flask run
```
The first command will activate a specialized Python environment for running Flask.
While the environment is activated, you should see a `(env)` prefix in the command prompt in your VM shell.
You should only run Flask while inside this environment; otherwise it will produce an error.

If you are running a local Vagrant VM, to view the app in your browser, you simply need to visit [http://localhost:5000/](http://localhost:5000/).
If you are running a Google VM, you will need to point your browser to `http://vm_external_ip_addr:5000/`, where `vm_external_ip_addr` is the external IP address of your Google VM.

To stop the website, simply press <kbd>Ctrl</kbd><kbd>C</kbd> in the VM shell where flask is running.
You can then deactivate the environment using
```
deactiviate
```

## Features of the Website

The website comes with all the basic functionalities of an Amazon-like ecommerce website:
* Users can register and log in with unique credentials and also change their personal info.
* Users can browse an array of products and add to their cart or save for later.
* Users can also easily become sellers to advertize and sell their own products.
* Users have a balance that they can top up to buy products or cash out; balance can also change when products are sold.
* Users can leave reviews and ratings for products and sellers and upvotes/downvotes for reviews as well.
* There are efficient input and selection validation checks throughout the backend process.
* The products display is neat and intuitive for user ease.

A full detailed list of the features can be found here: https://tinyurl.com/2p9a6dmc

## Working with the Project on Your Own

You can access the database directly by running the command `psql amazon` in your VM.

For debugging, you can access the database while the Flask server is running.
We recommend you open a second shell on your VM to run `psql amazon`.
After you perform some action on the website, you run a query inside `psql` to see the action has the intended effect on the database.

The `db/` subdirectory of this repository contains files useful for (re-)initializing the database if needed.
To (re-)initialize the database, first make sure that you are NOT running your Flask server or any `psql` sessions; then, from your repository directory, run `db/setup.sh`.
* You will see lots of text flying by---make sure you go through them carefully and verify there was no errors.
  Any error in (re-)initializing the database will cause your Flask server to fail, so make sure you fix them.
* If you get `ERROR:  database "amazon" is being accessed by other users`, that means you likely have Flask or another `psql` still running; terminate them and re-run `db/setup.sh`.
  If you cannot seem to find where you are running them, a sure way to get rid of them is to restart your VM.

To change the database schema, modify `db/create.sql` and `db/load.sql` as needed.
Make sure you to run `db/setup.sh` to reflect the changes.

Under `db/data/`, you will find CSV files that `db/load.sql` uses to initialize the database contents when you run `db/setup.sh`.
Under `db/generated/`, you will find alternate CSV files that will be used to initialize a bigger database instance when you run `db/setup.sh generated`; these files are automatically generated by running a script (which you can re-run by going inside `db/data/generated/` and running `python gen.py`.


We recommend Visual Studio Code (VS Code).
You can download and install it for your laptop from [this link](https://code.visualstudio.com/Download).

If you use a local Vagrant VM, we recommending placing your project directory under `~/shared/` so you can edit files using VS Code running on your laptop.

If you use a Google VM, your files live on the Google VM and you have no direct access to them.
However, you can still set up VS Code to edit the files directly via SSH.
See `README-vscode.md` in this repository for setup instructions.

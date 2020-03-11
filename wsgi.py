"""App entry point."""
from flask import Flask, jsonify, render_template, request, flash, send_file, g, redirect, session, url_for, Blueprint
from Permansys import create_app

app = create_app()
@app.route('/')
def index():
    return redirect('/app_tf.login')

if __name__ == "__main__":
    app.run(debug=True)

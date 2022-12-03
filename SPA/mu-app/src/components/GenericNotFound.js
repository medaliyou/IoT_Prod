
import React from "react";
import { Form, Button, Container, Alert } from 'react-bootstrap';
import { useParams, useNavigate } from "react-router-dom";

function GenericNotFound() {
  const navigate = useNavigate();

  return (

    <div className="card-body">
      <br>
      </br>
      <h2> Ooops ! </h2>
      <p>404 Page not found</p>
      <nav>
        <Button
          className="btn btn-primary nav-item active"
          onClick={() => navigate("/")}>
          Go Home
        </Button>
      </nav>


    </div>
  );
}


export default GenericNotFound;
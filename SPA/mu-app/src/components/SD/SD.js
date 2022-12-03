import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import AuthService, { MU_API, SD_API } from "../../services/auth.service"

import "../../App.css";


const SD = () => {

  const user = AuthService.getCurrentUser()



  const navigate = useNavigate();

  const [SDs, setSDs] = useState([]);



  const getSDs = () => {

    SD_API.get("SD/").then((response) => {
      console.log(response.data.data)
      setSDs(response.data.data);
    }).catch(error => {
      alert("Error Ocurred while loading data:" + error);
    });
  }


  React.useEffect(() => {

    if (null === user) {
      navigate("/", { replace: true });
    }
  }, [])




  useEffect(() => {
    getSDs();

  }, []);

  const authenticate = (pid_sd) => {
    MU_API.post("/app/v1/auth?PID_SD=" + pid_sd).then((response) => {
      alert("Smart Device PID= " + pid_sd + " authenticated to MU!");
      console.log(response)
      window.location.reload();

    }).catch(error => {
      alert("Error Ocurred in Smart Devices Authentication :" + error);
    });
  }

  const removeSD = (pid) => {
    SD_API.delete("/SD/PID/" + pid).then((response) => {
      alert("Smart Device PID= " + pid + " deleted!");
      getSDs();
      navigate('/SD')

    }).catch(error => {
      alert("Error Ocurred in Smart Devices:" + error);
    });

  }

  const removeAllSDs = (id) => {
    SD_API.delete("/SD/All").then((response) => {
      alert("All Smart Devices deleted!");
      getSDs();
      navigate('/SD')
    }).catch(error => {
      alert("Error Ocurred in Smart Devices:" + error);
    });
  }

  return (
    <div className="card-body">
      <br>
      </br>
      <nav>
        <button
          className="btn btn-primary nav-item active"
          onClick={() => navigate("/SD/create")}>
          Create New Smart Device
        </button>
      </nav>


      <br></br>
      <div className="col-md-12">
        <h4>Smart Devices List</h4>

        <div className="container">
          <div className="row">
            <div className="col-22">
              <table className="table table-bordered table-striped">
                <thead>
                  <tr>
                    <th>TAG</th>
                    <th>ID</th>
                    <th>PID</th>
                    <th>Session Key</th>

                    <th scope="col">Action</th>

                  </tr>
                </thead>
                <tbody>

                  {
                    SDs &&
                    SDs.map((sd, index) => (

                      <tr key={index}>
                        <th scope="row">{sd.TAG_SD}</th>
                        <td>{sd.ID_SD}</td>
                        <td>{sd.PID_SD}</td>
                        <td>{sd.SK === null ? "Not Authenticated yet": sd.SK}</td>

                        <td >

                          <button
                            onClick={() => removeSD(sd.PID_SD)}
                            className="btn btn-outline-danger"
                          > Delete
                          </button>
                          <button
                            onClick={() => authenticate(sd.PID_SD)}
                            className="btn btn-outline-primary"
                            disabled={sd.SK !== null}
                          > {sd.SK !== null ? "Authenticated" : "Authenticate"}
                          </button>
                        </td>
                      </tr>

                    ))
                  }

                </tbody>
              </table>
            </div>
          </div>
        </div>
        <button className="btn btn-sm btn-danger"
          onClick={() => removeAllSDs()}>
          Remove All
        </button>

      </div>

    </div>

  );
};

export default SD;
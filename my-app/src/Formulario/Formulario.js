import React, { useState, useEffect } from "react";
import { format } from "date-fns";
import "./formularioCSS.css";
import "./ButtonStyle.css";

function Formulario() {

  const [remitente, setRemitente] = useState("");
  const [correo, setEmail] = useState("");
  const [recogidaADomicilio, setRecogidaADomicilio] = useState(false);
  const [direccionRemitente, setDireccion_recogida] = useState("");
  const [destinatario, setDestinatario] = useState("");
  const [rutDestinatario, setRut_Destinatario] = useState("");
  const [fono, setFono] = useState("");

  const [fechaRecepcion, setFecha_de_recepcion] = useState("");
  const [ciudad, setCiudad] = useState("");
  const [codigoPostal, setCodigo_postal] = useState("");

  const [direccionEnvio, setDireccion_envio] = useState("");
  const [esSobre, setEs_sobre] = useState(false);
  const [porPagar, setPor_pagar] = useState(false);
  const [tipoEnvio, setTipo_de_envio] = useState("");
  const [peso, setPeso] = useState(0.0);
  const [repartoADomicilio, setReparto_a_domicilio] = useState(false);

  useEffect(() => {
    const fechaActual = new Date();
    const fechaFormateada = format(fechaActual, "dd/MM/yyyy");
    setFecha_de_recepcion(fechaFormateada);
  }, []);
  const validarCorreo = (email) => {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
  };
  const agregarGuionRut = (rut) => {
    if (rut.includes("-")) return rut;
    const rutConGuion = rut.slice(0, -1) + "-" + rut.slice(-1);
    return rutConGuion;
  };
  const handleChange = async (e) => {
    e.preventDefault();
    if (!validarCorreo(correo)) {
      alert("Por favor, ingrese un correo electrónico válido.");
      return;
    }
    try {
      const res = await fetch("http://127.0.0.1:5000/submit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          remitente,
          destinatario,
          fono,
          direccionEnvio,
          ciudad,
          tipoEnvio,
          correo,
          porPagar,
          fechaRecepcion,
          codigoPostal,
          esSobre,
          peso,
          recogidaADomicilio,
          direccionRemitente,
          repartoADomicilio,
          rutDestinatario,
          pagado: false,
          entregado: false
        }),
      });
      if (!res.ok) {
        throw new Error("Error al enviar datos al servidor");
      }
      const data = await res.json();
      console.log(data);
    } catch (error) {
      console.error("Error:", error.message);
    }
  };
  return (
    <form onSubmit={handleChange}>
      <section className="form-register">
        <div className="div_remitente">
          <h4>Datos Remitente</h4>
          <input
            className="controls"
            type="text"
            value={remitente}
            placeholder="Ingrese su nombre"
            onChange={(e) => setRemitente(e.target.value)}
          />
          <input
            className="controls"
            type="email"
            value={correo}
            placeholder="Ingrese su correo"
            onChange={(e) => setEmail(e.target.value)}
          />
          <label className="etiquetas" htmlFor="direccionRecogida">
            Recogida a domicilio
          </label>
          <select
            className="controls"
            value={recogidaADomicilio}
            onChange={(e) => setRecogidaADomicilio(e.target.value === "true")}
          >
            <option disabled value="">
              Seleccione una opción
            </option>
            <option value="true">Sí</option>
            <option value="false">No</option>
          </select>
          {recogidaADomicilio === true && (
            <input
              className="controls"
              type="text"
              value={direccionRemitente}
              placeholder="Ingrese su dirección de recogida"
              onChange={(e) => setDireccion_recogida(e.target.value)}
            />
          )}
        </div>
        <div className="div_destinatario">
          <h4>Datos del destinatario</h4>
          <input
            className="controls"
            type="text"
            value={destinatario}
            placeholder="Ingrese nombre del destinatario"
            onChange={(e) => setDestinatario(e.target.value)}
          />
          <input
            className="controls"
            type="text"
            value={rutDestinatario}
            placeholder="Ingrese Rut"
            onChange={(e) => setRut_Destinatario(e.target.value)}
          />
          <input
            className="controls"
            type="text"
            value={fono}
            placeholder="Numero de telefono"
            onChange={(e) => setFono(e.target.value)}
          />
          <label className="etiquetas" htmlFor="direccionRecogida">
            Reparto a domicilio
          </label>
          <select
            className="controls"
            value={repartoADomicilio}
            onChange={(e) => setReparto_a_domicilio(e.target.value === "true")}
          >
            <option disabled value="">
              Seleccione una opción
            </option>
            <option value="true">Sí</option>
            <option value="false">No</option>
          </select>
        </div>
        <div className="div_datos_envio">
          <h4>Datos de envio</h4>
          <input
            className="controls"
            type="text"
            value={direccionEnvio}
            placeholder="Ingrese la direccion"
            onChange={(e) => setDireccion_envio(e.target.value)}
          />
          <input
            className="controls"
            type="text"
            value={ciudad}
            placeholder="Ingrese ciudad"
            onChange={(e) => setCiudad(e.target.value)}
          />
          <input
            className="controls"
            type="text"
            value={codigoPostal}
            placeholder="Ingrese codigo postal"
            onChange={(e) => setCodigo_postal(e.target.value)}
          />
          <label className="etiquetas" htmlFor="tipo_entrega">
            Tipo de entrega
          </label>
          <select
            name="tipo_entrega"
            className="controls"
            onChange={(e) => setTipo_de_envio(e.target.value)}
          >
            <option disabled value="">
              Selecciona una opción
            </option>
            <option value="Entrega en el dia">Entrega en el día</option>
            <option value="Entrega rápida">Entrega rápida</option>
            <option value="Entrega normal">Entrega normal</option>
          </select>
          <label className="etiquetas" htmlFor="tipo_paquete">
            Tipo de paquete
          </label>
          <select
            name="tipo_paquete"
            className="controls"
            value={esSobre}
            onChange={(e) => setEs_sobre(e.target.value === "true")}
          >
            <option disabled value="">
              Selecciona una opción
            </option>
            <option value="true">Sobre</option>
            <option value="false">Encomienda</option>
          </select>
          {esSobre === false && (
            <React.Fragment>
              <label className="etiquetas" htmlFor="tipo_paquete">
                Indique peso en KG
              </label>
              <input
                className="controls"
                type="text"
                value={peso}
                onChange={(e) => setPeso(e.target.value)}
              />
            </React.Fragment>
          )}

          <label className="etiquetas" htmlFor="pago">
            Pagado por
          </label>
          <select
            name="pago"
            className="controls"
            value={porPagar ? "true" : "false"}
            onChange={(e) => setPor_pagar(e.target.value === "true")}
          >
            <option disabled selected hidden value="">
              Selecciona una opción
            </option>
            <option value="false">Remitente</option>
            <option value="true">Destinatario</option>
          </select>
        </div>
        <button href= "/envios"className="buttons" type="submit" value="Registrar">
        Registrar
        </button>
      </section>
    </form>
  );
}

export default Formulario;

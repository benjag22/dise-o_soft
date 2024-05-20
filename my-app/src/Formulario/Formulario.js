import React, { useState, useEffect } from "react";
import { format } from "date-fns";
import "./formularioCSS.css";
import "./ButtonStyle.css";

function Formulario() {
  const [Remitente, setRemitente] = useState("");
  const [Correo, setEmail] = useState("");
  const [Recogida_a_domicilio, setRecogidaADomicilio] = useState(false);
  const [Direccion_remitente, setDireccion_recogida] = useState("");
  const [Destinatario, setDestinatario] = useState("");
  const [Rut_Destinatario, setRut_Destinatario] = useState("");
  const [Fono, setFono] = useState("");

  const [Fecha_de_recepcion, setFecha_de_recepcion] = useState("");
  const [Ciudad, setCiudad] = useState("");
  const [Codigo_postal, setCodigo_postal] = useState("");

  const [Direccion_envio, setDireccion_envio] = useState("");
  const [Es_sobre, setEs_sobre] = useState(false);
  const [Por_pagar, setPor_pagar] = useState(false);
  const [Tipo_de_envio, setTipo_de_envio] = useState("");
  const [Peso, setPeso] = useState(0.0);
  const [Reparto_a_domicilio, setReparto_a_domicilio] = useState(false);

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
    if (!validarCorreo(Correo)) {
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
          Remitente,
          Destinatario,
          Fono,
          Direccion_envio,
          Ciudad,
          Tipo_de_envio,
          Correo,
          Por_pagar,
          Fecha_de_recepcion,
          Codigo_postal,
          Es_sobre,
          Peso,
          Recogida_a_domicilio,
          Direccion_remitente,
          Reparto_a_domicilio,
          Rut_Destinatario,
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
            value={Remitente}
            placeholder="Ingrese su nombre"
            onChange={(e) => setRemitente(e.target.value)}
          />
          <input
            className="controls"
            type="email"
            value={Correo}
            placeholder="Ingrese su correo"
            onChange={(e) => setEmail(e.target.value)}
          />
          <label className="etiquetas" htmlFor="direccionRecogida">
            Recogida a domicilio
          </label>
          <select
            className="controls"
            value={Recogida_a_domicilio}
            onChange={(e) => setRecogidaADomicilio(e.target.value === "true")}
          >
            <option disabled value="">
              Seleccione una opción
            </option>
            <option value="true">Sí</option>
            <option value="false">No</option>
          </select>
          {Recogida_a_domicilio === true && (
            <input
              className="controls"
              type="text"
              value={Direccion_remitente}
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
            value={Destinatario}
            placeholder="Ingrese nombre del destinatario"
            onChange={(e) => setDestinatario(e.target.value)}
          />
          <input
            className="controls"
            type="text"
            value={Rut_Destinatario}
            placeholder="Ingrese Rut"
            onChange={(e) => setRut_Destinatario(e.target.value)}
          />
          <input
            className="controls"
            type="text"
            value={Fono}
            placeholder="Numero de telefono"
            onChange={(e) => setFono(e.target.value)}
          />
          <label className="etiquetas" htmlFor="direccionRecogida">
            Reparto a domicilio
          </label>
          <select
            className="controls"
            value={Reparto_a_domicilio}
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
            value={Direccion_envio}
            placeholder="Ingrese la direccion"
            onChange={(e) => setDireccion_envio(e.target.value)}
          />
          <input
            className="controls"
            type="text"
            value={Ciudad}
            placeholder="Ingrese ciudad"
            onChange={(e) => setCiudad(e.target.value)}
          />
          <input
            className="controls"
            type="text"
            value={Codigo_postal}
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
            value={Es_sobre}
            onChange={(e) => setEs_sobre(e.target.value === "true")}
          >
            <option disabled value="">
              Selecciona una opción
            </option>
            <option value="true">Sobre</option>
            <option value="false">Encomienda</option>
          </select>
          {Es_sobre === false && (
            <React.Fragment>
              <label className="etiquetas" htmlFor="tipo_paquete">
                Indique peso en KG
              </label>
              <input
                className="controls"
                type="text"
                value={Peso}
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
            value={Por_pagar ? "true" : "false"}
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

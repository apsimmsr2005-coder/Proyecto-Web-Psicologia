const API_URL = "http://127.0.0.1:8000";

const state = {
  token: localStorage.getItem("saludmente_token"),
  usuario: JSON.parse(localStorage.getItem("saludmente_usuario") || "null"),
  beneficiarios: [],
  sesiones: [],
  seguimientos: [],
  usuarios: [],
};

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

function setMessage(message, isError = true) {
  const box = $("#appMessage");
  if (!box) return;
  box.textContent = message || "";
  box.style.color = isError ? "var(--warn)" : "var(--accent-strong)";
}

async function api(path, options = {}) {
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };
  if (state.token) {
    headers.Authorization = `Bearer ${state.token}`;
  }
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
  });
  const text = await response.text();
  const data = text ? JSON.parse(text) : null;
  if (!response.ok) {
    throw new Error(data?.detail || "Error en la solicitud");
  }
  return data;
}

function showLogin() {
  $("#loginView").classList.remove("hidden");
  $("#mainView").classList.add("hidden");
}

function showApp() {
  $("#loginView").classList.add("hidden");
  $("#mainView").classList.remove("hidden");
  $("#currentUser").textContent = state.usuario
    ? `${state.usuario.nombre} ${state.usuario.apellido} (${state.usuario.rol})`
    : "";
}

function showView(viewId) {
  $$(".tab").forEach((tab) => tab.classList.toggle("active", tab.dataset.view === viewId));
  $$(".view").forEach((view) => view.classList.toggle("active", view.id === viewId));
}

function formData(form) {
  return Object.fromEntries(new FormData(form).entries());
}

function resetForm(formId) {
  const form = document.getElementById(formId);
  form.reset();
  form.elements.id.value = "";
  [...form.elements].forEach((element) => {
    if (element.name === "identificador") element.disabled = false;
  });
}

function table(headers, rows) {
  if (!rows.length) {
    return `<div class="table-wrap"><table><tbody><tr><td>No hay registros.</td></tr></tbody></table></div>`;
  }
  return `
    <div class="table-wrap">
      <table>
        <thead>
          <tr>${headers.map((header) => `<th>${header}</th>`).join("")}</tr>
        </thead>
        <tbody>${rows.join("")}</tbody>
      </table>
    </div>
  `;
}

function optionList(items, labelFn, includeEmpty = false) {
  const empty = includeEmpty ? `<option value="">Sin asociar</option>` : "";
  return empty + items.map((item) => `<option value="${item.id}">${labelFn(item)}</option>`).join("");
}

function getBeneficiarioName(id) {
  const item = state.beneficiarios.find((beneficiario) => beneficiario.id === Number(id));
  return item ? `${item.nombre} ${item.apellido}` : `ID ${id}`;
}

function getUsuarioName(id) {
  const item = state.usuarios.find((usuario) => usuario.id === Number(id));
  return item ? `${item.nombre} ${item.apellido}` : `ID ${id}`;
}

async function loadAll() {
  setMessage("");
  const [usuarios, beneficiarios, sesiones, seguimientos] = await Promise.all([
    api("/usuarios/"),
    api("/beneficiarios/"),
    api("/sesiones/"),
    api("/seguimientos/"),
  ]);
  state.usuarios = usuarios;
  state.beneficiarios = beneficiarios;
  state.sesiones = sesiones;
  state.seguimientos = seguimientos;
  renderSelects();
  renderBeneficiarios();
  renderSesiones();
  renderSeguimientos();
  renderUsuarios();
  await renderDashboard();
}

async function renderDashboard() {
  const [resumen, beneficiariosEstado, sesionesEstado, cargaTerapeutas] = await Promise.all([
    api("/reportes/resumen"),
    api("/reportes/beneficiarios-por-estado"),
    api("/reportes/sesiones-por-estado"),
    api("/reportes/carga-terapeutas"),
  ]);

  const metrics = [
    ["Beneficiarios", resumen.total_beneficiarios],
    ["Casos activos", resumen.casos_activos],
    ["Sesiones realizadas", resumen.sesiones_realizadas],
    ["Seguimientos pendientes", resumen.seguimientos_pendientes],
    ["Riesgo alto", resumen.beneficiarios_riesgo_alto],
  ];
  $("#summaryGrid").innerHTML = metrics
    .map(([label, value]) => `<div class="metric"><span>${label}</span><strong>${value}</strong></div>`)
    .join("");

  $("#beneficiariosEstado").innerHTML = table(
    ["Estado", "Total"],
    beneficiariosEstado.map((row) => `<tr><td>${row.estado}</td><td>${row.total}</td></tr>`)
  );
  $("#sesionesEstado").innerHTML = table(
    ["Estado", "Total"],
    sesionesEstado.map((row) => `<tr><td>${row.estado}</td><td>${row.total}</td></tr>`)
  );
  $("#cargaTerapeutas").innerHTML = table(
    ["Terapeuta", "Total sesiones"],
    cargaTerapeutas.map((row) => `<tr><td>${row.terapeuta}</td><td>${row.total_sesiones}</td></tr>`)
  );
}

function renderSelects() {
  const beneficiarioOptions = optionList(
    state.beneficiarios,
    (item) => `${item.identificador} - ${item.nombre} ${item.apellido}`
  );
  const terapeutas = state.usuarios.filter((usuario) => ["admin", "terapeuta"].includes(usuario.rol));
  const terapeutaOptions = optionList(
    terapeutas,
    (item) => `${item.identificador} - ${item.nombre} ${item.apellido}`
  );
  const sesionOptions = optionList(
    state.sesiones,
    (item) => `${item.identificador} - ${item.fecha} ${item.hora}`,
    true
  );

  $("#sesionForm [name=beneficiario_id]").innerHTML = beneficiarioOptions;
  $("#sesionForm [name=terapeuta_id]").innerHTML = terapeutaOptions;
  $("#seguimientoForm [name=beneficiario_id]").innerHTML = beneficiarioOptions;
  $("#seguimientoForm [name=sesion_id]").innerHTML = sesionOptions;
}

function renderBeneficiarios() {
  const search = $("#beneficiarioSearch").value.trim().toLowerCase();
  const rows = state.beneficiarios
    .filter((item) => {
      const haystack = `${item.identificador} ${item.nombre} ${item.apellido} ${item.cedula}`.toLowerCase();
      return haystack.includes(search);
    })
    .map((item) => `
      <tr>
        <td>${item.identificador}</td>
        <td>${item.nombre} ${item.apellido}</td>
        <td>${item.cedula}</td>
        <td><span class="pill">${item.estado}</span></td>
        <td>${item.nivel_riesgo}</td>
        <td>${item.telefono}</td>
        <td class="actions">
          <button class="ghost-button" data-edit-beneficiario="${item.id}">Editar</button>
          <button class="danger-button" data-delete-beneficiario="${item.id}">Eliminar</button>
        </td>
      </tr>
    `);
  $("#beneficiariosTable").innerHTML = table(
    ["ID", "Nombre", "Cedula", "Estado", "Riesgo", "Telefono", "Acciones"],
    rows
  );
}

function renderSesiones() {
  const rows = state.sesiones.map((item) => `
    <tr>
      <td>${item.identificador}</td>
      <td>${getBeneficiarioName(item.beneficiario_id)}</td>
      <td>${getUsuarioName(item.terapeuta_id)}</td>
      <td>${item.fecha} ${item.hora}</td>
      <td>${item.modalidad}</td>
      <td><span class="pill">${item.estado}</span></td>
      <td class="actions">
        <button class="ghost-button" data-edit-sesion="${item.id}">Editar</button>
        <button class="danger-button" data-delete-sesion="${item.id}">Eliminar</button>
      </td>
    </tr>
  `);
  $("#sesionesTable").innerHTML = table(
    ["ID", "Beneficiario", "Terapeuta", "Fecha", "Modalidad", "Estado", "Acciones"],
    rows
  );
}

function renderSeguimientos() {
  const rows = state.seguimientos.map((item) => `
    <tr>
      <td>${item.identificador}</td>
      <td>${getBeneficiarioName(item.beneficiario_id)}</td>
      <td>${item.fecha}</td>
      <td>${item.prioridad}</td>
      <td>${item.completado ? "si" : "no"}</td>
      <td>${item.accion}</td>
      <td class="actions">
        <button class="ghost-button" data-edit-seguimiento="${item.id}">Editar</button>
        <button class="danger-button" data-delete-seguimiento="${item.id}">Eliminar</button>
      </td>
    </tr>
  `);
  $("#seguimientosTable").innerHTML = table(
    ["ID", "Beneficiario", "Fecha", "Prioridad", "Completado", "Accion", "Acciones"],
    rows
  );
}

function renderUsuarios() {
  const rows = state.usuarios.map((item) => `
    <tr>
      <td>${item.identificador}</td>
      <td>${item.nombre} ${item.apellido}</td>
      <td>${item.correo}</td>
      <td>${item.rol}</td>
      <td>${item.activo ? "si" : "no"}</td>
      <td class="actions">
        <button class="ghost-button" data-edit-usuario="${item.id}">Editar</button>
        <button class="danger-button" data-delete-usuario="${item.id}">Eliminar</button>
      </td>
    </tr>
  `);
  $("#usuariosTable").innerHTML = table(
    ["ID", "Nombre", "Correo", "Rol", "Activo", "Acciones"],
    rows
  );
}

function fillForm(formId, item, disabledIdentifier = true) {
  const form = document.getElementById(formId);
  Object.entries(item).forEach(([key, value]) => {
    if (form.elements[key] && value !== null && value !== undefined) {
      form.elements[key].value = value;
    }
  });
  if (disabledIdentifier && form.elements.identificador) {
    form.elements.identificador.disabled = true;
  }
}

function buildBeneficiarioPayload(form, isEdit) {
  const data = formData(form);
  const payload = {
    nombre: data.nombre,
    apellido: data.apellido,
    cedula: data.cedula,
    fecha_nacimiento: data.fecha_nacimiento,
    direccion: data.direccion,
    telefono: data.telefono,
    estado: data.estado,
    motivo_consulta: data.motivo_consulta,
    nivel_riesgo: data.nivel_riesgo,
  };
  if (!isEdit) payload.identificador = data.identificador;
  return payload;
}

function buildSesionPayload(form, isEdit) {
  const data = formData(form);
  const payload = {
    beneficiario_id: Number(data.beneficiario_id),
    terapeuta_id: Number(data.terapeuta_id),
    fecha: data.fecha,
    hora: data.hora,
    modalidad: data.modalidad,
    estado: data.estado,
    notas: data.notas,
  };
  if (!isEdit) payload.identificador = data.identificador;
  return payload;
}

function buildSeguimientoPayload(form, isEdit) {
  const data = formData(form);
  const payload = {
    beneficiario_id: Number(data.beneficiario_id),
    sesion_id: data.sesion_id ? Number(data.sesion_id) : null,
    fecha: data.fecha,
    descripcion: data.descripcion,
    accion: data.accion,
    prioridad: data.prioridad,
    completado: data.completado === "true",
  };
  if (!isEdit) payload.identificador = data.identificador;
  return payload;
}

function buildUsuarioPayload(form, isEdit) {
  const data = formData(form);
  if (!isEdit && !data.contrasena) {
    throw new Error("La contrasena es obligatoria para crear usuarios.");
  }
  const payload = {
    nombre: data.nombre,
    apellido: data.apellido,
    correo: data.correo,
    rol: data.rol,
    activo: data.activo === "true",
  };
  if (!isEdit) payload.identificador = data.identificador;
  if (data.contrasena) payload.contrasena = data.contrasena;
  return payload;
}

async function handleSubmit(formId, path, payloadBuilder, resetAfter = true) {
  const form = document.getElementById(formId);
  const id = form.elements.id.value;
  const isEdit = Boolean(id);
  const payload = payloadBuilder(form, isEdit);
  const method = isEdit ? "PUT" : "POST";
  const endpoint = isEdit ? `${path}/${id}` : `${path}/`;
  await api(endpoint, {
    method,
    body: JSON.stringify(payload),
  });
  if (resetAfter) resetForm(formId);
  await loadAll();
  setMessage("Registro guardado.", false);
}

async function removeItem(path, id) {
  await api(`${path}/${id}`, { method: "DELETE" });
  await loadAll();
  setMessage("Registro eliminado.", false);
}

function wireEvents() {
  $("#loginForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    $("#loginMessage").textContent = "";
    try {
      const data = await api("/auth/login", {
        method: "POST",
        body: JSON.stringify({
          correo: $("#loginCorreo").value,
          contrasena: $("#loginContrasena").value,
        }),
      });
      state.token = data.access_token;
      state.usuario = data.usuario;
      localStorage.setItem("saludmente_token", state.token);
      localStorage.setItem("saludmente_usuario", JSON.stringify(state.usuario));
      showApp();
      await loadAll();
    } catch (error) {
      $("#loginMessage").textContent = error.message;
    }
  });

  $("#logoutButton").addEventListener("click", () => {
    localStorage.removeItem("saludmente_token");
    localStorage.removeItem("saludmente_usuario");
    state.token = null;
    state.usuario = null;
    showLogin();
  });

  $$(".tab").forEach((tab) => tab.addEventListener("click", () => showView(tab.dataset.view)));

  $$("[data-reset]").forEach((button) => {
    button.addEventListener("click", () => resetForm(button.dataset.reset));
  });

  $("#beneficiarioSearch").addEventListener("input", renderBeneficiarios);

  $("#beneficiarioForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      await handleSubmit("beneficiarioForm", "/beneficiarios", buildBeneficiarioPayload);
    } catch (error) {
      setMessage(error.message);
    }
  });

  $("#sesionForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      await handleSubmit("sesionForm", "/sesiones", buildSesionPayload);
    } catch (error) {
      setMessage(error.message);
    }
  });

  $("#seguimientoForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      await handleSubmit("seguimientoForm", "/seguimientos", buildSeguimientoPayload);
    } catch (error) {
      setMessage(error.message);
    }
  });

  $("#usuarioForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      await handleSubmit("usuarioForm", "/usuarios", buildUsuarioPayload);
    } catch (error) {
      setMessage(error.message);
    }
  });

  document.body.addEventListener("click", async (event) => {
    const target = event.target;
    try {
      if (target.dataset.editBeneficiario) {
        const item = state.beneficiarios.find((row) => row.id === Number(target.dataset.editBeneficiario));
        fillForm("beneficiarioForm", item);
      }
      if (target.dataset.deleteBeneficiario) {
        await removeItem("/beneficiarios", target.dataset.deleteBeneficiario);
      }
      if (target.dataset.editSesion) {
        const item = state.sesiones.find((row) => row.id === Number(target.dataset.editSesion));
        fillForm("sesionForm", item);
      }
      if (target.dataset.deleteSesion) {
        await removeItem("/sesiones", target.dataset.deleteSesion);
      }
      if (target.dataset.editSeguimiento) {
        const item = state.seguimientos.find((row) => row.id === Number(target.dataset.editSeguimiento));
        fillForm("seguimientoForm", { ...item, completado: String(item.completado) });
      }
      if (target.dataset.deleteSeguimiento) {
        await removeItem("/seguimientos", target.dataset.deleteSeguimiento);
      }
      if (target.dataset.editUsuario) {
        const item = state.usuarios.find((row) => row.id === Number(target.dataset.editUsuario));
        fillForm("usuarioForm", { ...item, contrasena: "", activo: String(item.activo) });
      }
      if (target.dataset.deleteUsuario) {
        await removeItem("/usuarios", target.dataset.deleteUsuario);
      }
    } catch (error) {
      setMessage(error.message);
    }
  });
}

wireEvents();
if (state.token) {
  showApp();
  loadAll().catch((error) => {
    setMessage(error.message);
    showLogin();
  });
} else {
  showLogin();
}


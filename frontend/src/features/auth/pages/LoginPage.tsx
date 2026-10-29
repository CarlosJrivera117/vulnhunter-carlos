import { useState } from "react";
// Traemos la paleta de colores central del proyecto.
// Así el login usa los mismos colores que el resto del panel claro.
import { theme } from "../../../shared/styles/theme";

// Atajo para no escribir "theme.colors" en cada línea.
const c = theme.colors;

// Props que este componente recibe desde App.tsx:
// - onBack: vuelve a la pantalla de bienvenida (botón "← Volver").
// - onLogin: decide el rol (analyst o user) y entra al panel.
type LoginProps = {
  onBack: () => void;
  onLogin: (role: "analyst" | "user") => void;
};

function Login({ onBack, onLogin }: LoginProps) {
  // Estados del formulario (lo que el usuario escribe).
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // ---- LÓGICA DE LOGIN (se mantiene igual que antes) ----
  // Si el correo contiene "analista" -> entra como admin/analista.
  // Cualquier otro correo -> entra como usuario/cliente.
  // Más adelante esto se reemplaza por autenticación real del backend.
  const handleLogin = () => {
    if (email.toLowerCase().includes("analista")) {
      onLogin("analyst");
      return;
    }
    onLogin("user");
  };

  return (
    <main
      style={{
        minHeight: "100vh",
        width: "100%",
        // Fondo general claro (tomado del theme).
        backgroundColor: c.background,
        color: c.text,
        display: "flex",
        // En pantallas angostas las columnas se apilan.
        flexWrap: "wrap",
        fontFamily: "Inter, Arial, sans-serif",
      }}
    >
      {/* ================================================= */}
      {/* COLUMNA IZQUIERDA: formulario real (funcional)    */}
      {/* ================================================= */}
      <section
        style={{
          flex: "1 1 420px",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          padding: "48px",
        }}
      >
        <div style={{ width: "100%", maxWidth: "400px" }}>
          {/* Botón para volver a la pantalla anterior */}
          <button
            onClick={onBack}
            style={{
              backgroundColor: "transparent",
              border: "none",
              color: c.muted,
              cursor: "pointer",
              padding: 0,
              marginBottom: "28px",
              fontSize: "14px",
            }}
          >
            ← Volver
          </button>

          {/* Logo / marca */}
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "10px",
              marginBottom: "28px",
            }}
          >
            <div
              style={{
                width: "38px",
                height: "38px",
                borderRadius: "10px",
                backgroundColor: c.primary,
                color: "#FFFFFF",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontWeight: "bold",
                fontSize: "20px",
              }}
            >
              V
            </div>
            <span style={{ fontSize: "20px", fontWeight: 700 }}>
              VulnHunter
            </span>
          </div>

          {/* Títulos */}
          <h1 style={{ margin: "0 0 8px", fontSize: "28px" }}>
            Iniciar sesión
          </h1>
          <p
            style={{
              margin: "0 0 28px",
              color: c.muted,
              lineHeight: 1.6,
              fontSize: "15px",
            }}
          >
            Accede a tu panel para consultar tus análisis, hallazgos y
            reportes de seguridad.
          </p>

          {/* Campo: correo */}
          <label
            style={{
              display: "block",
              marginBottom: "8px",
              fontSize: "14px",
            }}
          >
            Correo electrónico
          </label>
          <input
            type="email"
            placeholder="usuario@empresa.cl"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{
              width: "100%",
              padding: "12px",
              borderRadius: "10px",
              border: `1px solid ${c.border}`,
              backgroundColor: "#FFFFFF",
              color: c.text,
              outline: "none",
              marginBottom: "20px",
              boxSizing: "border-box",
            }}
          />

          {/* Campo: contraseña */}
          <label
            style={{
              display: "block",
              marginBottom: "8px",
              fontSize: "14px",
            }}
          >
            Contraseña
          </label>
          <input
            type="password"
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{
              width: "100%",
              padding: "12px",
              borderRadius: "10px",
              border: `1px solid ${c.border}`,
              backgroundColor: "#FFFFFF",
              color: c.text,
              outline: "none",
              marginBottom: "24px",
              boxSizing: "border-box",
            }}
          />

          {/* Botón principal: se activa solo si hay correo y contraseña */}
          <button
            onClick={handleLogin}
            disabled={!email || !password}
            style={{
              width: "100%",
              backgroundColor: email && password ? c.primary : c.border,
              color: "#FFFFFF",
              border: "none",
              borderRadius: "10px",
              padding: "13px",
              cursor: email && password ? "pointer" : "not-allowed",
              fontWeight: 600,
              fontSize: "15px",
            }}
          >
            Iniciar sesión
          </button>

          {/* Botón decorativo de Google (NO funcional por ahora).
              Se conectará más adelante con autenticación real. */}
          <button
            disabled
            style={{
              width: "100%",
              marginTop: "12px",
              backgroundColor: "#FFFFFF",
              color: c.text,
              border: `1px solid ${c.border}`,
              borderRadius: "10px",
              padding: "13px",
              cursor: "not-allowed",
              fontWeight: 500,
              fontSize: "15px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: "8px",
            }}
          >
            <span style={{ fontWeight: 700, color: "#4285F4" }}>G</span>
            Continuar con Google (próximamente)
          </button>

          {/* Nota de desarrollo */}
          <p
            style={{
              marginTop: "22px",
              color: c.muted,
              fontSize: "12px",
              lineHeight: 1.6,
            }}
          >
            Acceso temporal para desarrollo. La autenticación real se
            implementará más adelante con el backend de VulnHunter.
          </p>
        </div>
      </section>

      {/* ================================================= */}
      {/* COLUMNA DERECHA: panel visual (SOLO DECORATIVO)   */}
      {/* Es una muestra de cómo se verá el producto.       */}
      {/* Ningún dato de aquí es real ni funcional.         */}
      {/* ================================================= */}
      <section
        style={{
          flex: "1 1 420px",
          backgroundColor: c.surface,
          borderLeft: `1px solid ${c.border}`,
          padding: "48px",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          gap: "20px",
        }}
      >
        <div>
          <h2 style={{ margin: "0 0 8px", fontSize: "22px" }}>
            Monitorea la seguridad de tus sitios
          </h2>
          <p style={{ margin: 0, color: c.muted, lineHeight: 1.6 }}>
            Escaneos automáticos, hallazgos priorizados por riesgo y
            reportes listos para descargar.
          </p>
        </div>

        {/* Tarjeta decorativa: reporte de ejemplo */}
        <div
          style={{
            backgroundColor: "#FFFFFF",
            border: `1px solid ${c.border}`,
            borderRadius: "14px",
            padding: "20px",
            boxShadow: "0 8px 24px rgba(15, 23, 42, 0.06)",
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: "16px",
            }}
          >
            <span style={{ fontWeight: 600 }}>Reporte de ejemplo</span>
            {/* Score de riesgo (decorativo) */}
            <span
              style={{
                backgroundColor: "#FEF2F2",
                color: c.severity.high,
                padding: "4px 10px",
                borderRadius: "999px",
                fontSize: "13px",
                fontWeight: 600,
              }}
            >
              Riesgo 72 · Alto
            </span>
          </div>

          {/* Lista de hallazgos de ejemplo */}
          {[
            { label: "Inyección SQL", sev: "Crítica", color: c.severity.critical, bg: "#FEF2F2" },
            { label: "XSS reflejado", sev: "Alta", color: c.severity.high, bg: "#FFF7ED" },
            { label: "Headers faltantes", sev: "Media", color: c.severity.medium, bg: "#FEFCE8" },
            { label: "TLS débil", sev: "Baja", color: c.severity.low, bg: "#F0FDF4" },
          ].map((f) => (
            <div
              key={f.label}
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                padding: "10px 0",
                borderTop: `1px solid ${c.border}`,
              }}
            >
              <span style={{ fontSize: "14px" }}>{f.label}</span>
              <span
                style={{
                  backgroundColor: f.bg,
                  color: f.color,
                  padding: "2px 10px",
                  borderRadius: "999px",
                  fontSize: "12px",
                  fontWeight: 600,
                }}
              >
                {f.sev}
              </span>
            </div>
          ))}
        </div>

        {/* Tarjeta decorativa: "escaneando" */}
        <div
          style={{
            backgroundColor: "#FFFFFF",
            border: `1px solid ${c.border}`,
            borderRadius: "14px",
            padding: "18px",
            display: "flex",
            alignItems: "center",
            gap: "12px",
            boxShadow: "0 8px 24px rgba(15, 23, 42, 0.06)",
          }}
        >
          <div
            style={{
              width: "10px",
              height: "10px",
              borderRadius: "50%",
              backgroundColor: c.primary,
            }}
          />
          <div>
            <div style={{ fontSize: "14px", fontWeight: 600 }}>
              Escaneando tienda-ejemplo.cl…
            </div>
            <div style={{ fontSize: "12px", color: c.muted }}>
              Analizando SSL, cabeceras y formularios
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}

export default Login;

import { useState, useEffect } from "react";
import { api } from "./services/api";
import type { Tarefa, StatusTarefa } from "./types";
import "./index.css";

function App() {
  const [tasks, setTasks] = useState<Tarefa[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const [isFormOpen, setIsFormOpen] = useState<boolean>(false);
  const [editingTask, setEditingTask] = useState<Tarefa | null>(null);
  
  // Form state
  const [titulo, setTitulo] = useState<string>("");
  const [descricao, setDescricao] = useState<string>("");

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.get<Tarefa[]>("/tarefas");
      setTasks(response.data);
    } catch (err: any) {
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError("Erro ao conectar com o servidor.");
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const openNewForm = () => {
    setTitulo("");
    setDescricao("");
    setEditingTask(null);
    setIsFormOpen(true);
  };

  const openEditForm = (task: Tarefa) => {
    setTitulo(task.titulo);
    setDescricao(task.descricao);
    setEditingTask(task);
    setIsFormOpen(true);
  };

  const closeForm = () => {
    setIsFormOpen(false);
    setEditingTask(null);
    setTitulo("");
    setDescricao("");
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!titulo.trim() || !descricao.trim()) {
      alert("Título e descrição são obrigatórios.");
      return;
    }

    try {
      setError(null);
      if (editingTask) {
        await api.put(`/tarefas/${editingTask.id}`, { titulo, descricao });
      } else {
        await api.post("/tarefas", { titulo, descricao });
      }
      closeForm();
      fetchTasks();
    } catch (err: any) {
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError("Erro ao salvar tarefa.");
      }
    }
  };

  const handleChangeStatus = async (id: number, newStatus: StatusTarefa) => {
    try {
      setError(null);
      await api.patch(`/tarefas/${id}/status`, { status: newStatus });
      fetchTasks();
    } catch (err: any) {
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError("Erro ao alterar status.");
      }
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm("Tem certeza que deseja excluir esta tarefa?")) {
      return;
    }

    try {
      setError(null);
      await api.delete(`/tarefas/${id}`);
      fetchTasks();
    } catch (err: any) {
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError("Erro ao excluir tarefa.");
      }
    }
  };

  return (
    <div className="container">
      <h1>Tarefas</h1>

      {error && <div className="error-message">{error}</div>}

      {!isFormOpen && (
        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <button className="btn" onClick={openNewForm}>Nova tarefa</button>
        </div>
      )}

      {isFormOpen && (
        <div className="form-container">
          <h2>{editingTask ? "Editar Tarefa" : "Nova Tarefa"}</h2>
          <form onSubmit={handleSave}>
            <div className="form-group">
              <label>Título</label>
              <input
                type="text"
                value={titulo}
                onChange={(e) => setTitulo(e.target.value)}
                placeholder="Ex: Minha tarefa"
              />
            </div>
            <div className="form-group">
              <label>Descrição</label>
              <textarea
                rows={3}
                value={descricao}
                onChange={(e) => setDescricao(e.target.value)}
                placeholder="Ex: Descrição da tarefa"
              ></textarea>
            </div>
            <div style={{ display: "flex", gap: "1rem" }}>
              <button type="submit" className="btn">Salvar</button>
              <button type="button" className="btn btn-secondary" onClick={closeForm}>Cancelar</button>
            </div>
          </form>
        </div>
      )}

      {!isFormOpen && (
        <div className="task-list">
          {loading && <div className="loading">Carregando tarefas...</div>}
          
          {!loading && tasks.length === 0 && (
            <div className="empty-state">Nenhuma tarefa cadastrada.</div>
          )}

          {!loading && tasks.map((task) => (
            <div className="task-item" key={task.id}>
              <div className="task-header">
                <div className="task-title">{task.titulo}</div>
                <div className={`status-badge ${
                  task.status === "PENDENTE" ? "status-pendente" :
                  task.status === "EM_ANDAMENTO" ? "status-em-andamento" :
                  "status-concluida"
                }`}>
                  {task.status.replace("_", " ")}
                </div>
              </div>
              <div className="task-description">{task.descricao}</div>
              
              <div className="task-actions">
                <button className="btn btn-secondary" onClick={() => openEditForm(task)}>Editar</button>
                <button className="btn btn-danger" onClick={() => handleDelete(task.id)}>Excluir</button>
                
                <div className="task-status">
                  <label style={{ marginLeft: "0.5rem", fontWeight: 600 }}>Status:</label>
                  <select 
                    value={task.status} 
                    onChange={(e) => handleChangeStatus(task.id, e.target.value as StatusTarefa)}
                  >
                    <option value="PENDENTE">Pendente</option>
                    <option value="EM_ANDAMENTO">Em Andamento</option>
                    <option value="CONCLUIDA">Concluída</option>
                  </select>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;

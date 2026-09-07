export type StatusTarefa = "PENDENTE" | "EM_ANDAMENTO" | "CONCLUIDA";

export interface Tarefa {
  id: number;
  titulo: string;
  descricao: string;
  status: StatusTarefa;
}

export interface TarefaCreate {
  titulo: string;
  descricao: string;
}

export interface TarefaUpdate {
  titulo?: string;
  descricao?: string;
}

export interface TarefaStatusUpdate {
  status: StatusTarefa;
}

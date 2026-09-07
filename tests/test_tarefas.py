def test_criar_tarefa(client):
    response = client.post("/tarefas", json={
        "titulo": "Tarefa de teste",
        "descricao": "Descrição da tarefa de teste"
    })
    # Validações baseadas no endpoint atual da API
    assert response.status_code in (200, 201)
    data = response.json()
    assert "id" in data
    assert data["titulo"] == "Tarefa de teste"
    assert data["descricao"] == "Descrição da tarefa de teste"
    assert data["status"] == "PENDENTE"

def test_listar_tarefas(client):
    # Setup de dados local
    client.post("/tarefas", json={"titulo": "T1", "descricao": "D1"})
    
    response = client.get("/tarefas")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(t["titulo"] == "T1" for t in data)

def test_buscar_tarefa_por_id(client):
    cria_resp = client.post("/tarefas", json={"titulo": "T2", "descricao": "D2"})
    tarefa_id = cria_resp.json()["id"]

    response = client.get(f"/tarefas/{tarefa_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == tarefa_id
    assert data["titulo"] == "T2"

def test_buscar_tarefa_inexistente(client):
    response = client.get("/tarefas/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Tarefa não encontrada"

def test_atualizar_tarefa(client):
    cria_resp = client.post("/tarefas", json={"titulo": "Velho", "descricao": "Velho"})
    tarefa_id = cria_resp.json()["id"]

    response = client.put(f"/tarefas/{tarefa_id}", json={
        "titulo": "Tarefa atualizada",
        "descricao": "Descrição atualizada"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == "Tarefa atualizada"
    assert data["descricao"] == "Descrição atualizada"
    assert data["status"] == "PENDENTE" # Status continua

def test_alterar_status(client):
    cria_resp = client.post("/tarefas", json={"titulo": "T3", "descricao": "D3"})
    tarefa_id = cria_resp.json()["id"]

    # Atualiza 1
    resp1 = client.patch(f"/tarefas/{tarefa_id}/status", json={"status": "EM_ANDAMENTO"})
    assert resp1.status_code == 200
    assert resp1.json()["status"] == "EM_ANDAMENTO"

    # Atualiza 2
    resp2 = client.patch(f"/tarefas/{tarefa_id}/status", json={"status": "CONCLUIDA"})
    assert resp2.status_code == 200
    assert resp2.json()["status"] == "CONCLUIDA"

def test_deletar_tarefa(client):
    cria_resp = client.post("/tarefas", json={"titulo": "T4", "descricao": "D4"})
    tarefa_id = cria_resp.json()["id"]

    del_resp = client.delete(f"/tarefas/{tarefa_id}")
    assert del_resp.status_code == 204

    get_resp = client.get(f"/tarefas/{tarefa_id}")
    assert get_resp.status_code == 404

def test_deletar_tarefa_inexistente(client):
    response = client.delete("/tarefas/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Tarefa não encontrada"

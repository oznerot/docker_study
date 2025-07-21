# Projeto Kubernetes com Helm - CRUD de Estudantes

Este projeto consiste em um CRUD completo utilizando:
- **MongoDB** como banco de dados
- **FastAPI** como backend (API REST)
- **Angular** como frontend, servido via **Nginx**
- **Kubernetes** para orquestração
- **Helm** para gerenciamento dos manifestos

## 📦 Estrutura dos Diretórios

```
student-app/
├── charts/              
├── templates/
│   ├── mongodb/           # Manifests do MongoDB
│   ├── api/               # Manifests da API
│   ├── frontend/          # Manifests do frontend Angular
│   └── ingress/           # Ingress NGINX
├── values.yaml            # Variáveis globais do Helm
└── Chart.yaml             # Definição do chart
```

## Como Executar

1. Clone o repositório e entre no diretório do projeto Helm:

```bash
git clone https://github.com/oznerot/docker_study.git
cd docker_study/student-app
```

2. Inicie o Minikube:

```bash
minikube start
```

3. Ative o tunnel do Minikube (em outro terminal):

```bash
minikube tunnel
```

4. Instale o controlador do Ingress:

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace
```

5. Instale a aplicação com Helm:

```bash
helm install student-app .
```

6. Mapeie o External IP para k8s.local

```bash
kubectl get svc -n ingress-nginx
sudo nano /etc/hosts
```

7. Adicione essa linha no final do arquivo
```text
<EXTERNAL-IP> k8s.local
```

8. Acesse http://k8s.local/

## Como Atualizar

Se fizer alterações no código, recompile as imagens, suba para o Docker Hub e depois:

```bash
helm upgrade student-app .
```

## Como Deletar os Containers

```bash
helm uninstall student-app
kubectl delete namespace ingress-nginx
```

## Em Caso de Problemas

- Verifique se o `minikube tunnel` está ativo
- Confirme se as imagens estão no Docker Hub e públicas
- Use `kubectl get pods`, `kubectl describe pod <nome>` e `kubectl logs <nome>` para debugar
- Use `kubectl get ingress` e `kubectl describe ingress` para verificar o roteamento
- Verifique o IP do Ingress com:

```bash
kubectl get svc -n ingress-nginx
```

## Observações

- O frontend é servido na raiz (`/`) e a API em `/api`
- As configurações de CORS e `root_path` já estão preparadas para Kubernetes
- O Ingress faz o roteamento baseado nos paths e o NGINX interno do Angular serve os arquivos estáticos

from flask import Flask, make_response, request

app = Flask(__name__)

FLAG = "FLAG{xss_roubou_o_cookie}"


@app.route("/")
def home():
    resposta = make_response(
        """
        <h1>Loja do Renan</h1>
        <p>Digite seu nome para receber um ola:</p>
        <form action="/ola">
          <input name="nome" placeholder="seu nome">
          <button type="submit">Enviar</button>
        </form>
        """
    )
    resposta.set_cookie("sessao", FLAG, httponly=False)
    return resposta


@app.route("/ola")
def ola():
    nome = request.args.get("nome", "visitante")
    return f"<h1>Ola, {nome}!</h1><a href='/'>Voltar</a>"


if __name__ == "__main__":
    app.run()
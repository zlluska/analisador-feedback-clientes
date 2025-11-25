"""
Analisador Inteligente de Feedback de Clientes
Usa a API da OpenAI para análise de sentimento e categorização
Autor: Lucas Fraga + Claude.ia
GitHub: https://github.com/zlluska/analisador-feedback-clientes
"""

import os
import json
from openai import OpenAI
from typing import List, Dict
from datetime import datetime

class FeedbackAnalyzer:
    def __init__(self, api_key: str = None):
        """
        Inicializa o analisador com a chave da API OpenAI
        
        Args:
            api_key: Chave da API OpenAI (opcional, pode usar variável de ambiente)
        """
        self.client = OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
        self.feedbacks = []
        self.results = []
    
    def add_feedback(self, text: str, author: str, source: str = "manual"):
        """
        Adiciona um novo feedback à lista para análise
        
        Args:
            text: Texto do feedback do cliente
            author: Nome do autor do feedback
            source: Origem do feedback (email, whatsapp, chat, etc)
        """
        feedback = {
            "id": len(self.feedbacks) + 1,
            "text": text,
            "author": author,
            "source": source,
            "timestamp": datetime.now().isoformat()
        }
        self.feedbacks.append(feedback)
        print(f"✅ Feedback #{feedback['id']} adicionado: {author}")
    
    def analyze_feedback(self, text: str) -> Dict:
        """
        Analisa um feedback individual usando a API da OpenAI
        
        Args:
            text: Texto do feedback a ser analisado
            
        Returns:
            Dicionário com sentimento, resumo, categoria e prioridade
        """
        prompt = f"""Analise o seguinte feedback de cliente e retorne APENAS um objeto JSON no formato:
{{
  "sentimento": "Positivo" ou "Negativo" ou "Neutro",
  "resumo": "breve resumo do problema ou elogio principal em até 100 caracteres",
  "categoria": "Atendimento" ou "Produto" ou "Entrega" ou "Preço" ou "Outro",
  "prioridade": "Alta" ou "Média" ou "Baixa"
}}

Feedback: "{text}"
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um especialista em análise de sentimento e atendimento ao cliente. Sempre responda apenas com JSON válido."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            # Extrai e limpa a resposta
            result_text = response.choices[0].message.content.strip()
            result_text = result_text.replace("```json", "").replace("```", "").strip()
            
            return json.loads(result_text)
        
        except Exception as e:
            print(f"❌ Erro ao analisar feedback: {e}")
            return {
                "sentimento": "Erro",
                "resumo": "Não foi possível analisar este feedback",
                "categoria": "Outro",
                "prioridade": "Baixa"
            }
    
    def analyze_all(self):
        """
        Analisa todos os feedbacks da lista usando IA
        """
        if not self.feedbacks:
            print("⚠️  Nenhum feedback para analisar. Adicione feedbacks primeiro.")
            return
        
        print(f"\n🔄 Analisando {len(self.feedbacks)} feedbacks...\n")
        
        self.results = []
        for feedback in self.feedbacks:
            print(f"Analisando feedback #{feedback['id']} de {feedback['author']}...")
            analysis = self.analyze_feedback(feedback['text'])
            
            # Combina dados do feedback original com a análise
            result = {
                **feedback,
                **analysis
            }
            self.results.append(result)
            
            # Exibe resultado com emoji
            emoji = "😊" if analysis['sentimento'] == "Positivo" else "😠" if analysis['sentimento'] == "Negativo" else "😐"
            print(f"{emoji} {analysis['sentimento']} | {analysis['categoria']} | {analysis['resumo']}\n")
        
        print("✅ Análise concluída!\n")
    
    def get_statistics(self) -> Dict:
        """
        Calcula estatísticas dos feedbacks analisados
        
        Returns:
            Dicionário com estatísticas (total, positivos, negativos, etc)
        """
        if not self.results:
            return {}
        
        stats = {
            "total": len(self.results),
            "positivos": len([r for r in self.results if r['sentimento'] == "Positivo"]),
            "negativos": len([r for r in self.results if r['sentimento'] == "Negativo"]),
            "neutros": len([r for r in self.results if r['sentimento'] == "Neutro"]),
            "categorias": {},
            "prioridades": {}
        }
        
        # Conta por categoria
        for result in self.results:
            cat = result['categoria']
            stats['categorias'][cat] = stats['categorias'].get(cat, 0) + 1
            
            prior = result.get('prioridade', 'Baixa')
            stats['prioridades'][prior] = stats['prioridades'].get(prior, 0) + 1
        
        return stats
    
    def print_report(self):
        """
        Imprime um relatório completo e formatado da análise
        """
        if not self.results:
            print("⚠️  Nenhuma análise realizada. Execute analyze_all() primeiro.")
            return
        
        print("\n" + "="*60)
        print("📊 RELATÓRIO DE ANÁLISE DE FEEDBACKS")
        print("="*60)
        
        stats = self.get_statistics()
        
        # Estatísticas gerais
        print(f"\n📈 Total de feedbacks analisados: {stats['total']}")
        print(f"😊 Positivos: {stats['positivos']} ({stats['positivos']/stats['total']*100:.1f}%)")
        print(f"😠 Negativos: {stats['negativos']} ({stats['negativos']/stats['total']*100:.1f}%)")
        print(f"😐 Neutros: {stats['neutros']} ({stats['neutros']/stats['total']*100:.1f}%)")
        
        # Por categoria
        print("\n📋 Feedbacks por categoria:")
        for cat, count in stats['categorias'].items():
            print(f"  • {cat}: {count} ({count/stats['total']*100:.1f}%)")
        
        # Por prioridade
        print("\n🎯 Feedbacks por prioridade:")
        for prior, count in stats['prioridades'].items():
            print(f"  • {prior}: {count}")
        
        # Feedbacks negativos (requerem atenção)
        negativos = [r for r in self.results if r['sentimento'] == "Negativo"]
        if negativos:
            print("\n⚠️  FEEDBACKS NEGATIVOS (Requerem Atenção!):")
            for neg in negativos:
                print(f"\n  🔴 {neg['author']} ({neg['source']})")
                print(f"      \"{neg['text'][:80]}...\"")
                print(f"      → {neg['resumo']}")
                print(f"      → Prioridade: {neg['prioridade']}")
        
        # Feedbacks positivos (destaque)
        positivos = [r for r in self.results if r['sentimento'] == "Positivo"]
        if positivos:
            print("\n✨ FEEDBACKS POSITIVOS (Pontos Fortes!):")
            for pos in positivos[:3]:  # Mostra até 3
                print(f"\n  🟢 {pos['author']}")
                print(f"      → {pos['resumo']}")
        
        print("\n" + "="*60)
    
    def export_to_json(self, filename: str = "feedback_results.json"):
        """
        Exporta todos os resultados para um arquivo JSON
        
        Args:
            filename: Nome do arquivo de saída (padrão: feedback_results.json)
        """
        if not self.results:
            print("⚠️  Nenhum resultado para exportar.")
            return
        
        data = {
            "results": self.results,
            "statistics": self.get_statistics(),
            "export_date": datetime.now().isoformat(),
            "total_feedbacks": len(self.results)
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Resultados exportados para '{filename}'")
    
    def export_to_csv(self, filename: str = "feedback_results.csv"):
        """
        Exporta resultados para CSV (opcional, requer pandas)
        
        Args:
            filename: Nome do arquivo CSV
        """
        try:
            import pandas as pd
            
            df = pd.DataFrame(self.results)
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"💾 Resultados exportados para '{filename}'")
        
        except ImportError:
            print("⚠️  Pandas não está instalado. Use: pip install pandas")


def main():
    """
    Função principal - Demonstração do uso do analisador
    """
    print("="*60)
    print("🚀 ANALISADOR INTELIGENTE DE FEEDBACK DE CLIENTES")
    print("="*60)
    print("\nUsando IA para análise automática de sentimento\n")
    
    # Inicializa o analisador
    # A API key pode vir da variável de ambiente OPENAI_API_KEY
    analyzer = FeedbackAnalyzer()
    
    # Feedbacks de exemplo (simulando diferentes fontes)
    feedbacks_exemplo = [
        {
            "text": "O atendimento foi excelente! A equipe resolveu meu problema rapidamente e com muita atenção. Recomendo!",
            "author": "João Silva",
            "source": "email"
        },
        {
            "text": "Produto chegou com defeito e o suporte demora muito para responder. Muito insatisfeito com a experiência!",
            "author": "Maria Santos",
            "source": "whatsapp"
        },
        {
            "text": "Preço justo, entrega no prazo. Nada de especial, mas também não tenho reclamações.",
            "author": "Pedro Costa",
            "source": "formulário web"
        },
        {
            "text": "Adorei o produto! Superou minhas expectativas. A qualidade é ótima e chegou antes do previsto.",
            "author": "Ana Oliveira",
            "source": "email"
        },
        {
            "text": "Fiz o pedido há 2 semanas e ainda não recebi. Tentei contato pelo chat mas ninguém responde. Péssimo!",
            "author": "Carlos Mendes",
            "source": "chat online"
        },
        {
            "text": "Gostei do atendimento, mas achei o preço um pouco alto comparado à concorrência.",
            "author": "Juliana Lima",
            "source": "telefone"
        }
    ]
    
    # Adiciona todos os feedbacks
    print("📥 Adicionando feedbacks...\n")
    for fb in feedbacks_exemplo:
        analyzer.add_feedback(fb['text'], fb['author'], fb['source'])
    
    # Analisa todos os feedbacks
    analyzer.analyze_all()
    
    # Exibe relatório completo
    analyzer.print_report()
    
    # Exporta resultados
    analyzer.export_to_json()
    
    print("\n✅ Processo concluído!")
    print("💡 Dica: Você pode adicionar mais feedbacks e analisar novamente.")


if __name__ == "__main__":
    # Verifica se a API key está configurada
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  ATENÇÃO: Variável de ambiente OPENAI_API_KEY não encontrada!")
        print("Configure sua API key antes de executar:")
        print("  Windows: set OPENAI_API_KEY=sua-chave-aqui")
        print("  Mac/Linux: export OPENAI_API_KEY=sua-chave-aqui")
        print("\nOu crie um arquivo .env com:")
        print("  OPENAI_API_KEY=sua-chave-aqui\n")
    else:
        main()
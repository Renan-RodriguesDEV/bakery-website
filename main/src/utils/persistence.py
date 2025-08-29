import streamlit as st
import extra_streamlit_components as stx
import json
import time
from src.utils.uteis import Logger

class CookieSessionManager:
    def __init__(self, cookie_name="bakery_session", expiry_days=30):
        self.cookie_name = cookie_name
        self.expiry_days = expiry_days
        self.cookie_manager = stx.CookieManager()
    
    def save_session(self, user_data):
        """Salva os dados da sessão em cookie e session_state"""
        try:
            # Set cookie with expiration
            self.cookie_manager.set(
                self.cookie_name,
                json.dumps(user_data),
                expires_at=int(time.time() + self.expiry_days*86400)
            )
            
            # Update session state
            for key, value in user_data.items():
                st.session_state[key] = value
            
            Logger.info(f"Sessão salva com sucesso para {user_data.get('username')}")
            return True
        except Exception as e:
            Logger.error(f"Erro ao salvar sessão em cookie: {e}")
            return False
    
    def load_session(self):
        """Carrega os dados da sessão do cookie para session_state"""
        try:
            session_data = self.cookie_manager.get(self.cookie_name)
            
            if session_data:
                session_data = json.loads(session_data)
                
                # Update session state with cookie data
                for key, value in session_data.items():
                    st.session_state[key] = value
                
                Logger.info(f"Sessão carregada com sucesso para {session_data.get('username')}")
                return True
            
            return False
        except Exception as e:
            Logger.error(f"Erro ao carregar sessão do cookie: {e}")
            return False
    
    def clear_session(self):
        """Remove os dados da sessão do cookie"""
        try:
            self.cookie_manager.delete(self.cookie_name)
            Logger.info("Cookie de sessão removido com sucesso")
            return True
        except Exception as e:
            Logger.error(f"Erro ao remover cookie de sessão: {e}")
            return False
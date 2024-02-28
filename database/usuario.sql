

CREATE TABLE public."usuario" (
	id int8 NOT NULL DEFAULT nextval('usuario_id'::regclass),
	nome varchar(100) NOT NULL,
	email varchar(100) NOT NULL,
	senha text NOT NULL,
	cpf varchar(15) NOT NULL,
	foto text NULL,
	status bool NOT NULL DEFAULT true,
	created_at timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamp(3) NOT NULL,
	deleted_at timestamp(3) NULL,
	"uuid" varchar(36) NULL,
	CONSTRAINT "Usuario_pkey" PRIMARY KEY (id)
);
CREATE UNIQUE INDEX "Usuario_email_key" ON public."usuario-asd" USING btree (email);
CREATE INDEX "Usuario_nome_cpf_created_at_updated_at_idx" ON public."usuario-asd" USING btree (nome, cpf, created_at, updated_at);
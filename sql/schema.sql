create table if not exists deputados (
    id integer primary key,
    nome text not null,
    sigla_uf char(2),
    url_foto text
);

create table if not exists votacoes (
    id text primary key,
    data date not null,
    descricao text,
    aprovacao boolean,
    id_proposicao integer
);

create table if not exists votos (
    id_votacao text not null references votacoes (id),
    id_deputado integer not null references deputados (id),
    tipo_voto text not null,
    sigla_partido text,
    primary key (id_votacao, id_deputado)
);

create index if not exists idx_votos_deputado on votos (id_deputado);
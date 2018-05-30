rm databases/*
psql << EOF
DROP DATABASE sigulab2;
CREATE DATABASE sigulab2;
EOF

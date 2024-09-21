{% macro create_index(table_name, columns) %}
    {% if columns is string %}
        {% set columns = [columns] %}
    {% endif %}
    
    {% set column_list = columns | join(', ') %}
    
    CREATE INDEX IF NOT EXISTS idx_{{ table_name }}
        ON dev_stage.{{ table_name }} ({{ column_list }});
{% endmacro %}
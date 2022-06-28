#include "modbus.h"
#include <QtSql/QSql>
#include <QtSql/QSqlDatabase>
#include <QtSql/QSqlQuery>

modbus::modbus(QString host, uint16_t port)
{
    HOST = host;
    PORT = port;
    _slaveid = 1;
    _msg_id = 1;
    _connected = false;
    flagTask = true;
    socket = new QTcpSocket();
}

modbus::modbus(QString host)
{
    modbus(host, 502);
}

modbus::~modbus(void)
{
    flagTask = false;
}

void  modbus::modbus_set_slave_id(int id)
{
    _slaveid = id;
}

bool  modbus::modbus_connect()
{
    if (HOST == "" || PORT == 0)
    {
        if (MODBUS_DEBUG) qDebug() << "Missing Host and Port";
        return false;
    }
    else
    {
        if (MODBUS_DEBUG) qDebug() << "Found Proper Host " << HOST << " and Port " << PORT;
    }

    //socket = new QTcpSocket();

    socket->connectToHost(HOST, PORT);

    if (!socket->waitForConnected(1000))
    {
        if (MODBUS_DEBUG) qDebug() << "Connection Error";
        //socket->deleteLater();
        return false;
    }

    if (MODBUS_DEBUG) qDebug() << "Connected";
    _connected = true;
    return true;
}

void  modbus::modbus_close()
{
    socket->disconnectFromHost();
    if (MODBUS_DEBUG) qDebug() << "Socket Closed -->" << HOST;
}

void  modbus::modbus_build_request(uint8_t *to_send, int address, int func)
{
    //to_send[0] = (uint8_t) _msg_id >> 8;
    to_send[0] = _msg_id >> 8;
    to_send[1] = (uint8_t)(_msg_id & 0x00FF);
    to_send[2] = 0;
    to_send[3] = 0;
    to_send[4] = 0;
    to_send[6] = (uint8_t) _slaveid;
    to_send[7] = (uint8_t) func;
    to_send[8] = (uint8_t)(address >> 8);
    to_send[9] = (uint8_t)(address & 0x00FF);
}

void  modbus::modbus_write(int address, int amount, int func, uint16_t *value)
{
    if (func == WRITE_COIL || func == WRITE_REG)
    {
        uint8_t to_send[12];
        modbus_build_request(to_send, address, func);
        to_send[5] = 6;
        to_send[10] = (uint8_t)(value[0] >> 8);
        to_send[11] = (uint8_t)(value[0] & 0x00FF);
        modbus_send(to_send, 12);
    }
    else if (func == WRITE_REGS)
    {
        uint8_t *to_send;
        //uint8_t to_send[13 + 2 * amount];
        to_send = new uint8_t[13 + 2 * amount];
        modbus_build_request(to_send, address, func);
        to_send[5] = (uint8_t)(5 + 2 * amount);
        to_send[10] = (uint8_t)(amount >> 8);
        to_send[11] = (uint8_t)(amount & 0x00FF);
        to_send[12] = (uint8_t)(2 * amount);
        for (int i = 0; i < amount; i++)
        {
            to_send[13 + 2 * i] = (uint8_t)(value[i] >> 8);
            to_send[14 + 2 * i] = (uint8_t)(value[i] & 0x00FF);
        }
        modbus_send(to_send, 13 + 2 * amount);
        delete[] to_send; //when finish
    }
    else if (func == WRITE_COILS)
    {
        uint8_t *to_send;
        //uint8_t to_send[14 + (amount -1) / 8 ];
        to_send = new uint8_t[14 + (amount - 1) / 8];
        modbus_build_request(to_send, address, func);
        to_send[5] = (uint8_t)(7 + (amount - 1) / 8);
        to_send[10] = (uint8_t)(amount >> 8);
        to_send[11] = (uint8_t)(amount >> 8);
        to_send[12] = (uint8_t)((amount + 7) / 8);
        for (int i = 0; i < amount; i++)
        {
            to_send[13 + (i - 1) / 8] += (uint8_t)(value[i] << (i % 8));
        }
        modbus_send(to_send, 14 + (amount - 1) / 8);
        delete[] to_send; //when finish
    }
}

void  modbus::modbus_read(int address, int amount, int func)
{
    uint8_t to_send[12];
    modbus_build_request(to_send, address, func);
    to_send[5] = 6;
    to_send[10] = (uint8_t)(amount >> 8);
    to_send[11] = (uint8_t)(amount & 0x00FF);
    modbus_send(to_send, 12);
}

void  modbus::modbus_read_holding_registers(int address, int amount, uint16_t *buffer)
{
    if (_connected)
    {
        if (amount > 65535 || address > 65535)
        {
            //throw modbus_amount_exception();
        }
        modbus_read(address, amount, READ_REGS);
        uint8_t to_rec[MAX_MSG_LENGTH];
        qint64 k = modbus_receive(to_rec);
        try
        {
            modbus_error_handle(to_rec, READ_REGS);
            for (int i = 0; i < amount; i++)
            {
                buffer[i] = ((uint16_t)to_rec[9 + 2 * i]) << 8;
                buffer[i] += (uint16_t) to_rec[10 + 2 * i];
            }
        }
        catch (std::exception &e)
        {
            if (MODBUS_DEBUG) qDebug() << e.what();
            delete[](&to_rec);
            delete(&k);
            throw e;
        }
    }
    else
    {
        //throw modbus_connect_exception();
    }
}

void  modbus::modbus_read_input_registers(int address, int amount, uint16_t *buffer)
{
    if (_connected)
    {
        if (amount > 65535 || address > 65535)
        {
            //throw modbus_amount_exception();
        }
        modbus_read(address, amount, READ_INPUT_REGS);
        uint8_t to_rec[MAX_MSG_LENGTH];
        qint64 k = modbus_receive(to_rec);
        try
        {
            modbus_error_handle(to_rec, READ_INPUT_REGS);
            for (int i = 0; i < amount; i++)
            {
                buffer[i] = ((uint16_t)to_rec[9 + 2 * i]) << 8;
                buffer[i] += (uint16_t) to_rec[10 + 2 * i];
            }
        }
        catch (std::exception &e)
        {
            if (MODBUS_DEBUG) qDebug() << e.what();
            delete[](&to_rec);
            delete(&k);
            throw e;
        }
    }
    else
    {
        //throw modbus_connect_exception();
    }
}

void  modbus::modbus_read_coils(int address, int amount, bool *buffer)
{
    if (_connected)
    {
        if (amount > 2040 || address > 65535)
        {
            //throw modbus_amount_exception();
        }
        modbus_read(address, amount, READ_COILS);
        uint8_t to_rec[MAX_MSG_LENGTH];
        qint64 k = modbus_receive(to_rec);
        try
        {
            modbus_error_handle(to_rec, READ_COILS);
            for (int i = 0; i < amount; i++)
            {
                buffer[i] = (bool)((to_rec[9 + i / 8] >> (i % 8)) & 1);
            }
        }
        catch (std::exception &e)
        {
            if (MODBUS_DEBUG) qDebug() << e.what();
            delete[](&to_rec);
            delete(&k);
            throw e;
        }
    }
    else
    {
        //throw modbus_connect_exception();
    }
}

void  modbus::modbus_read_input_bits(int address, int amount, bool* buffer)
{
    if (_connected)
    {
        if (amount > 2040 || address > 65535)
        {
            //throw modbus_amount_exception();
        }
        modbus_read(address, amount, READ_INPUT_BITS);
        uint8_t to_rec[MAX_MSG_LENGTH];
        qint64 k = modbus_receive(to_rec);
        try
        {
            modbus_error_handle(to_rec, READ_INPUT_BITS);
            for (int i = 0; i < amount; i++)
            {
                buffer[i] = (bool)((to_rec[9 + i / 8] >> (i % 8)) & 1);
            }
        }
        catch (std::exception &e)
        {
            if (MODBUS_DEBUG) qDebug() << e.what();
            delete[](&to_rec);
            delete(&k);
            throw e;
        }
    }
    else
    {
        //throw modbus_connect_exception();
    }
}

void  modbus::modbus_write_coil(int address, bool to_write)
{
    if (_connected)
    {
        if (address > 65535)
        {
            //throw modbus_amount_exception();
        }
        int value = to_write * 0xFF00;
        modbus_write(address, 1, WRITE_COIL, (uint16_t *)&value);
        uint8_t to_rec[MAX_MSG_LENGTH];
        qint64 k = modbus_receive(to_rec);
        try
        {
            modbus_error_handle(to_rec, WRITE_COIL);
        }
        catch (std::exception &e)
        {
            if (MODBUS_DEBUG) qDebug() << e.what();
            delete[](&to_rec);
            delete(&k);
            throw e;
        }
    }
    else
    {
        //throw modbus_connect_exception();
    }
}

void  modbus::modbus_write_register(int address, uint16_t value)
{
    if (_connected)
    {
        if (address > 65535)
        {
            //throw modbus_amount_exception();
        }
        modbus_write(address, 1, WRITE_REG, &value);
        uint8_t to_rec[MAX_MSG_LENGTH];
        qint64 k = modbus_receive(to_rec);
        try
        {
            modbus_error_handle(to_rec, WRITE_COIL);
        }
        catch (std::exception &e)
        {
            if (MODBUS_DEBUG) qDebug() << e.what();
            delete[](&to_rec);
            delete(&k);
            throw e;
        }
    }
    else
    {
        //throw modbus_connect_exception();
    }
}

void  modbus::modbus_write_coils(int address, int amount, bool *value)
{
    if (_connected)
    {
        if (address > 65535 || amount > 65535)
        {
            //throw modbus_amount_exception();
        }
        uint16_t * temp;
        temp = new uint16_t[amount];
        //uint16_t temp[amount];
        for (int i = 0; i < 4; i++)
        {
            temp[i] = (uint16_t)value[i];
        }
        modbus_write(address, amount, WRITE_COILS, temp);
        uint8_t to_rec[MAX_MSG_LENGTH];
        qint64 k = modbus_receive(to_rec);
        delete[] temp;
        try
        {
            modbus_error_handle(to_rec, WRITE_COILS);
        }
        catch (std::exception &e)
        {
            if (MODBUS_DEBUG) qDebug() << e.what();
            delete[](&to_rec);
            delete(&k);
            throw e;
        }
    }
    else
    {
        //throw modbus_connect_exception();
    }
}

void  modbus::modbus_write_registers(int address, int amount, uint16_t *value)
{
    if (_connected)
    {
        if (address > 65535 || amount > 65535)
        {
            //throw modbus_amount_exception();
        }
        modbus_write(address, amount, WRITE_REGS, value);
        uint8_t to_rec[MAX_MSG_LENGTH];
        qint64 k = modbus_receive(to_rec);
        try
        {
            modbus_error_handle(to_rec, WRITE_REGS);
        }
        catch (std::exception &e)
        {
            if (MODBUS_DEBUG) qDebug() << e.what();
            delete[](&to_rec);
            delete(&k);
            throw e;
        }
    }
    else
    {
        //throw modbus_connect_exception();
    }
}

qint64 modbus::modbus_send(uint8_t *to_send, int length)
{
    _msg_id++;
    QByteArray to_send_byte = QByteArray(reinterpret_cast<char*>(to_send), length);
    quint64 s = socket->write(to_send_byte);
    socket->waitForBytesWritten(500);
    return s;
}

qint64 modbus::modbus_receive(uint8_t *buffer)
{
    //return recv(_socket, (char *) buffer, 1024, 0);
    socket->waitForReadyRead(500);
    quint64 len = socket->bytesAvailable();
    if (len > 0)
    {
        QByteArray rxByteArray = socket->readAll();
        memcpy(buffer, rxByteArray, rxByteArray.length());
    }
    //quint64 s = socket->read((char *)buffer, 1024);
    //socket->waitForReadyRead(100);
    return len;
}

void modbus::modbus_error_handle(uint8_t *msg, int func)
{
    if (msg[7] == (func + 0x80))
    {
        err_code = msg[8];
        switch (msg[8])
        {
        case EX_ILLEGAL_FUNCTION:
            if (MODBUS_DEBUG) qDebug() << "throw modbus_illegal_function_exception()";
            break;
        case EX_ILLEGAL_ADDRESS:
            if (MODBUS_DEBUG) qDebug() << "throw modbus_illegal_address_exception()";
            break;
        case EX_ILLEGAL_VALUE:
            if (MODBUS_DEBUG) qDebug() << "throw modbus_illegal_data_value_exception()";
            break;
        case EX_SERVER_FAILURE:
            if (MODBUS_DEBUG) qDebug() << "throw modbus_server_failure_exception()";
            break;
        case EX_ACKNOWLEDGE:
            if (MODBUS_DEBUG) qDebug() << "throw modbus_acknowledge_exception()";
            break;
        case EX_SERVER_BUSY:
            if (MODBUS_DEBUG) qDebug() << "throw modbus_server_busy_exception()";
            break;
        case EX_GATEWAY_PROBLEMP:
        case EX_GATEWYA_PROBLEMF:
            if (MODBUS_DEBUG) qDebug() << "throw modbus_gateway_exception()";
            break;
        default:
            break;
        }
    }
    else err_code = 0;
}

void modbus::modbus_debug(bool flag)
{
    MODBUS_DEBUG = flag;
}

void modbus::Test()
{
    qDebug() << "Hello from DLL";
}

void modbus::run()
{
    socket = new QTcpSocket();

    while (flagTask)
    {
       if(writeCommand1 != "")
       {
           readCommand1 = plc_write(writeCommand1);
           writeCommand1 = "";
       }
       else if(writeCommand2 != "")
       {
           if(writeCommand2 == "set_D1_timer")
           {
               _d1time = dtime;
           }
           if(writeCommand2 == "set_D2_timer")
           {
               _d2time = dtime;
           }

           readCommand2 = plc_write(writeCommand2, dtime);
           writeCommand2 = "";
       }
       else
       {
            readValue = plc_read();
       }
       msleep(100);
    }
}

QString modbus::plc_read()
{
    bool read_bits[8];
    bool read_bits_y[8];
    uint16_t read_regs[2];
    QJsonDocument json_doc;
    QJsonObject root_obj = json_doc.object();
    err_code = 0;

    if(modbus_connect())
    {
        modbus_read_holding_registers(4116, 2, read_regs);
        //modbus_read_holding_registers(20, 2, read_regs);
        if(err_code == 0)
        {
            modbus_read_input_bits(1280, 8, read_bits_y);
        }
        if(err_code == 0)
        {
            modbus_read_input_bits(1024, 8, read_bits);
        }
        if(err_code == 0)
        {
            root_obj.insert("zone1", read_bits[0]);
            root_obj.insert("zone2", read_bits[1]);
            root_obj.insert("zone3", read_bits[2]);
            root_obj.insert("zone4", read_bits[3]);
            root_obj.insert("zone5", read_bits[4]);
            root_obj.insert("door1", read_bits[5]);
            root_obj.insert("door2", read_bits[6]);

            root_obj.insert("key", read_bits[7]);
            root_obj.insert("err_code", err_code);
            root_obj.insert("flash", read_bits_y[2]);
            root_obj.insert("D1Time", read_regs[0]);
            root_obj.insert("D2Time", read_regs[1]);
            root_obj.insert("led", read_bits_y[4]);
            root_obj.insert("regula_out", read_bits_y[3]);
        }
        else
        {
            err_code = EX_CONNECT_PROBLEM;
            root_obj.insert("err_code", err_code);
        }

        json_doc = QJsonDocument(root_obj);
        modbus_close();
    }
    else
    {
        err_code = EX_CONNECT_PROBLEM;
        root_obj.insert("err_code", err_code);
        json_doc = QJsonDocument(root_obj);
    }

    return json_doc.toJson(QJsonDocument::Compact);
}

QString modbus::plc_write(QString command, uint16_t time)
{
    int e_code = 0;
    QJsonDocument json_doc;
    QJsonObject root_obj = json_doc.object();

    if(modbus_connect())
    {
        if(time >= 1 && time <= 30)
        {
            if(command.compare("set_D1_timer") == 0)
            {
                modbus_write_register(4116, time);
            }
            else if(command.compare("set_D2_timer") == 0)
            {
                modbus_write_register(4117, time);
            }
            else
            {
                e_code = EX_COMMAND_PROBLEM;
            }
        }
        else
        {
            e_code = EX_ILLEGAL_TIME_VALUE;
        }


        modbus_close();
    }
    else
    {
        e_code = EX_CONNECT_PROBLEM;
    }

    if(e_code != 0)
    {
        root_obj.insert("err_code", e_code);
        json_doc = QJsonDocument(root_obj);
    }
    else if(err_code != 0)
    {
        root_obj.insert("err_code", err_code);
        json_doc = QJsonDocument(root_obj);
    }
    else
    {
        root_obj.insert("err_code", err_code);
        json_doc = QJsonDocument(root_obj);
    }


    return json_doc.toJson(QJsonDocument::Compact);

}

QString modbus::plc_write(QString command)
{
    int e_code = 0;
    uint16_t door_regs[2];
    QJsonDocument json_doc;
    QJsonObject root_obj = json_doc.object();

    door_regs[0] = _d1time;
    door_regs[1] = _d2time;

    if(modbus_connect())
    {
        if(command.compare("door1_open") == 0)
        {
            modbus_write_coil(1280, true);
        }
        else if(command.compare("door2_open") == 0)
        {
            modbus_write_coil(1281, true);
        }
        else if(command.compare("door1_close") == 0)
        {
            modbus_write_coil(1280, false);
        }
        else if(command.compare("door2_close") == 0)
        {
            modbus_write_coil(1281, false);
        }
        else if(command.compare("all_open") == 0)
        {
            modbus_write_coil(1280, true);
            modbus_write_coil(1281, true);
        }
        else if(command.compare("all_close") == 0)
        {
            modbus_write_coil(1280, false);
            modbus_write_coil(1281, false);
        }
        else if(command.compare("flash_on") == 0)
        {
            modbus_write_coil(1282, true);
        }
        else if(command.compare("flash_off") == 0)
        {
            modbus_write_coil(1282, false);
        }
        else if(command.compare("led_active") == 0)
        {
            modbus_write_coil(1284, true);
        }
        else if(command.compare("led_inactive") == 0)
        {
            modbus_write_coil(1284, false);
        }
        else if(command.compare("regula_reset") == 0)
        {
            modbus_write_coil(1283, true);
        }
        else if(command.compare("set_door_time") == 0)
        {
            modbus_write_register(4116, door_regs[0]);
            modbus_write_register(4117, door_regs[1]);
        }
        else
        {
            e_code = EX_COMMAND_PROBLEM;
        }
        modbus_close();
    }
    else
    {
        e_code = EX_CONNECT_PROBLEM;
    }

    if(e_code != 0)
    {
        root_obj.insert("err_code", e_code);
        json_doc = QJsonDocument(root_obj);
    }
    else if(err_code != 0)
    {
        root_obj.insert("err_code", err_code);
        json_doc = QJsonDocument(root_obj);
    }
    else
    {
        root_obj.insert("err_code", err_code);
        json_doc = QJsonDocument(root_obj);
    }

    return json_doc.toJson(QJsonDocument::Compact);
}

void modbus::msleep(int msec)
{
    QEventLoop loop;
    QTimer::singleShot(msec, &loop, &QEventLoop::quit);
    loop.exec();
}
